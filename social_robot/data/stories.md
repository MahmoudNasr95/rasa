## happy path
* greet
  - utter_greet
  - utter_askstate
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
  - utter_askstate
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
  - utter_askstate
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## answer state
* ask_state
  - utter_botstate
  - utter_askstate


## answer state
* ask_state
  - utter_botstate
  - utter_askstate

## Fedi story
* greet
  - utter_greet
  - utter_askstate
* mood_great
  - utter_happy
* tell_fedi
  - utter_fedi
* goodbye
  - utter_goodbye

## story_01
* greet
  - utter_greet
* introduce
  - utter_introduce
  - utter_askstate
* mood_great
  - utter_happy

## story_01a
* greet
  - utter_greet
  - utter_getIdentity
* introduce
  - utter_introduce
  - utter_askstate
* mood_great
  - utter_happy


## story_02
* introduce
  - utter_introduce
  - utter_askstate
* mood_great
  - utter_happy

## story_02a
* introduce
  - utter_introduce
  - utter_askstate
* mood_unhappy
  - utter_cheer_up

## move_action1
* greet
  - utter_greet
  - utter_offer_help
* move_cmd
  - action_move
  - utter_job_done


## move_action1
* greet
  - utter_greet
  - utter_getIdentity
* introduce
  - utter_introduce
  - utter_offer_help
* move_cmd
  - action_move
  - utter_job_done
* thanks
  - utter_welcome

## action_1
* move_cmd
  - action_move
  - utter_job_done

## help_ok
* move_cmd
  - action_move
  - utter_job_done
* affirm
  - utter_happy 

## help_ok
* move_cmd
  - action_move
  - utter_job_done
* mood_great
  - utter_happy 

## Add_Med Story 1
* greet
  - utter_greet
  - utter_offer_help
* add_med
  - action_get_med
  - utter_job_done

## Add_Med Story 1a
* greet
  - utter_greet
* add_med
  - action_get_med
  - utter_job_done

## Move Story
* greet
  - utter_greet
  - utter_getIdentity
* introduce
  - utter_introduce
  - utter_askstate
* mood_great
  - utter_happy
  - utter_offer_help
* move_cmd
  - action_move
  - utter_job_status_enquiry
* affirm
  - utter_happy

## Generated Story 1687739553500467122
* greet
    - utter_greet
* introduce{"name": "Wissem"}
    - slot{"name": "Wissem"}
    - utter_introduce
    - utter_askstate
* mood_great
    - utter_happy
    - utter_offer_help
* goodbye
    - utter_goodbye

## Generated Story 1216236861617122270
* greet
    - utter_greet
* introduce{"name": "Mahmoud"}
    - slot{"name": "Mahmoud"}
    - utter_introduce
    - utter_askstate
* mood_great
    - utter_happy
    - utter_offer_help
* add_med{"med_name": "beta", "day": "Friday"}
    - action_get_med
    - utter_job_done

## Generated Story -3619287370097992977
* greet
    - utter_greet
* introduce
    - rewind
* introduce{"name": "mahmoud"}
    - slot{"name": "mahmoud"}
    - utter_introduce
    - utter_askstate
* deny
    - utter_cheer_up
* thanks
    - utter_welcome
* goodbye
    - utter_goodbye

## Generated Story 3039982268169413311
* greet
    - utter_greet
* ask_state
    - utter_botstate
    - utter_askstate
* mood_great
    - utter_happy
    - utter_offer_help

## Generated Story 809759528725163918
* greet
    - utter_greet
* add_med{"day": "friday", "DATE": "friday"}
    - rewind
* add_med{"med_name": "y", "day": "friday", "DATE": "friday"}
    - action_get_med
    - utter_job_done
* thanks
    - utter_welcome

## Generated Story -3083396129647270154
* greet
    - utter_greet
* add_med{"med_name": "X", "number": "3", "TIME": "3 am"}
    - action_get_med
    - utter_job_done
* thanks
    - utter_welcome
