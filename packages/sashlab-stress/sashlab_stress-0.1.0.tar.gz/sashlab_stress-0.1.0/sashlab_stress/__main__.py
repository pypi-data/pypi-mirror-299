import argparse
import keyboard as kb
import time
from datetime import datetime, timedelta
import winsound
from .attention import attention_check
from .clear_prompt import clear_terminal
from .trial import trial
from .Participant import Participant, MakeParticipant
from .difficulty_manager import DifficultyManager
from .RoundInfo import Round
from .log_rounds import log_session
import pathlib as pl


def main():
    clear_terminal()
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Run the app with optional parameters.")
    parser.add_argument("--time-limit", type=int, default=300, help="Time limit for the session in seconds")
    parser.add_argument("--trial-time", type=int, default=15, help="Number of seconds before each individual trial timesout from a lack of interaction")
    parser.add_argument("--path", type=pl.Path, default=pl.Path().cwd(), help="The path where the session data will be saved")
    args = parser.parse_args()


    print("Session set up:")
    print(f"Session duration: {args.time_limit/60} minutes")
    print(f"Trial timeout limit: {args.trial_time}")
    participant: Participant = MakeParticipant()

    attention_counter = 0
    while not attention_check() and attention_counter < 5:
        attention_counter += 1
        if attention_counter >= 5:
            print("You have failed the attention check too many times")
            time.sleep(1)
            winsound.Beep(880, 2200)
            break

    participant.set_attention_fails(attention_counter)

    print(f"Participant id = {participant.id}")
    print(f"Attenttion failures = {participant.attention_fails}")

    print(
        """
        In the next section subtraction problems will appear on screen. Please solve the problem by entering your answer to the problem and then pressing enter. Ensure to only enter numeric characters.\n

        Press the Spacebar when you're ready to continue
        """
    )

    kb.wait(hotkey="spacebar")
    participant.set_start_time()
    clear_terminal()

    d = DifficultyManager()
    round = 1
    rounds = []

    while True:
        clear_terminal()
        if not (datetime.now() - participant.start_time) >= timedelta(seconds=args.time_limit):
            r = Round(round ,d.difficulty, (datetime.now() - participant.start_time) )
            try:
                print(f"Round {round}")
                print(f"You are playing at difficulty level {d.get_difficulty()-1}")
                answer = trial(d.get_difficulty(), n_seconds=args.trial_time)
                print(answer)
                d.update_streaks(answer)
                d.update_difficulty()
                r.set_answer(answer)
                round +=1 
                
                time.sleep(1)
            except KeyboardInterrupt:
                print("Finished testing")
                break
            finally:
                rounds.append(r)

        else:
            print("This activity is finished")
            break

    log_session(participant, rounds, args.path)

if __name__ == "__main__":
    main()
