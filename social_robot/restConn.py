class RestInput(InputChannel):
	"""A custom http input channel.

	This implementation is the basis for a custom implementation of a chat
	frontend. You can customize this to send messages to Rasa Core and
	retrieve responses from the agent."""

	@classmethod
	def name(cls):
		return "rest"

	@staticmethod
	async def on_message_wrapper(
		on_new_message: Callable[[UserMessage], Awaitable[None]],
		text: Text,
		queue: Queue,
		sender_id: Text,
	) -> None:
		collector = QueueOutputChannel(queue)

		message = UserMessage(
			text, collector, sender_id, input_channel=RestInput.name()
		)
		await on_new_message(message)

		await queue.put("DONE")  # pytype: disable=bad-return-type

	async def _extract_sender(self, req) -> Optional[Text]:
		return req.json.get("sender", None)

	# noinspection PyMethodMayBeStatic
	def _extract_message(self, req):
		return req.json.get("message", None)

	def stream_response(
		self,
		on_new_message: Callable[[UserMessage], Awaitable[None]],
		text: Text,
		sender_id: Text,
	) -> Callable[[Any], Awaitable[None]]:
		async def stream(resp: Any) -> None:
			q = Queue()
			task = asyncio.ensure_future(
				self.on_message_wrapper(on_new_message, text, q, sender_id)
			)
			while True:
				result = await q.get()  # pytype: disable=bad-return-type
				if result == "DONE":
					break
				else:
					await resp.write(json.dumps(result) + "\n")
			await task

		return stream  # pytype: disable=bad-return-type

	def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[None]]):
		custom_webhook = Blueprint(
			"custom_webhook_{}".format(type(self).__name__),
			inspect.getmodule(self).__name__,
		)

		# noinspection PyUnusedLocal
		@custom_webhook.route("/", methods=["GET"])
		async def health(request: Request):
			return response.json({"status": "ok"})

		@custom_webhook.route("/webhook", methods=["POST"])
		async def receive(request: Request):
			sender_id = await self._extract_sender(request)
			text = self._extract_message(request)
			should_use_stream = rasa.utils.endpoints.bool_arg(
				request, "stream", default=False
			)

			if should_use_stream:
				return response.stream(
					self.stream_response(on_new_message, text, sender_id),
					content_type="text/event-stream",
				)
			else:
				collector = CollectingOutputChannel()
				# noinspection PyBroadException
				try:
					await on_new_message(
						UserMessage(
							text, collector, sender_id, input_channel=self.name()
						)
					)
				except CancelledError:
					logger.error(
						"Message handling timed out for "
						"user message '{}'.".format(text)
					)
				except Exception:
					logger.exception(
						"An exception occured while handling "
						"user message '{}'.".format(text)
					)
				return response.json(collector.messages)

		return custom_webhook