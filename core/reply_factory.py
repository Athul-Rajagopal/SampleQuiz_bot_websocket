from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["current_question_id"] = 0  # Set current_question_id to 0 if it's None
        session.save()
        return bot_responses

    current_question_id = int(current_question_id)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to the Django session.
    '''
    # Get the current question from the question list
    current_question = PYTHON_QUESTION_LIST[current_question_id]

    # Get the correct answer for the current question
    correct_answer = current_question['answer']

    # Validate the user's answer against the correct answer
    if answer == correct_answer:
        # Store the user's answer in the session
        session['user_answers'] = session.get('user_answers', {})
        session['user_answers'][current_question_id] = answer
        session.save()
        return True, "Good job!"
    else:
        return False, "Incorrect answer. Please try again."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
        return next_question, next_question_id
    else:
        return None, None  # No more questions available


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    user_answers = session.get('user_answers', {})
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = sum(1 for q_id, q in enumerate(PYTHON_QUESTION_LIST) if user_answers.get(str(q_id)) == q['answer'])

    # Calculate the user's score
    score = (correct_answers / total_questions) * 100

    # Generate final response message
    final_response = f"Congratulations on completing the quiz!\nYou answered {correct_answers} out of {total_questions} questions correctly.\nYour score is {score}%."

    return final_response
