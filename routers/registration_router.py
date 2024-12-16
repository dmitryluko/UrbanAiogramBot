from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db.db_manager import DatabaseManager
from service.users import is_user_exists, add_user
from states.registration_state import RegistrationState

# Initialize the router and database manager
registration_router = Router()
db_manager = DatabaseManager('users')


# Registration start function
@registration_router.message(F.text == 'Registration')
async def sign_up(message: Message, state: FSMContext):
    """
    :param message: The incoming message from the user triggering the registration process.
    :param state: FSMContext object to manage the finite state of the user during the registration process.
    :return: None
    """
    await message.answer('Enter User Name : ')
    await state.set_state(RegistrationState.username)


# Handler to set username
@registration_router.message(RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    """
    :param message: Incoming message from the user.
    :param state: FSM (Finite State Machine) context to manage conversation states.
    :return: None. The method performs asynchronous operations such as sending a message to the user and updating FSM context.

    """
    username = message.text

    # Check if username exists in the database
    if is_user_exists(db_manager, username):
        await message.answer('User is exists. Try another username: ')
    else:
        # Save username in FSM context
        await state.update_data(username=username)
        await message.answer('Enter E-Mail address: ')
        await state.set_state(RegistrationState.email)


# Handler to set email
@registration_router.message(RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    """
    :param message: The incoming message containing user input, specifically the email address in this context.
    :param state: The finite state machine context used to store and manage user data and the current state of the registration process.
    :return: None
    """
    email = message.text
    # Save email in FSM context
    await state.update_data(email=email)
    await message.answer('How old are you? : ')
    await state.set_state(RegistrationState.age)


# Handler to set age and finish the registration process
@registration_router.message(RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    """
    :param message: The message received from the user. Contains the text inputted for age.
    :param state: FSMContext instance used to retrieve temporary data and manage the finite state machine context.
    :return: None
    """
    age = int(message.text)

    # Retrieve all the data from the FSM context
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')

    # Add the user to the database (default balance = 1000)
    add_user(db_manager,
             username=username,
             email=email,
             age=age)

    # Clear the FSM and finish the registration process
    await state.clear()

    await message.answer(f'Registration completed! Welcome, {username}!')
