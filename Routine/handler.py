import threading
import datetime
from time import sleep
from Routine.markup import *
from Base.markup import *
from Routine.message import *
from Base.message import *
from Routine.models import Activity
import uuid




last_bot_message = {}
bot_status = 0
waiting_for_input_id = None  


def unset_status():
    while True:
        now_time = datetime.datetime.now().strftime("%H:%M")
        if now_time == "00:00":
            Activity.reset_all_status()
        sleep(60)


def handle(bot):

    def bot_action(msg, call, *args):
        global waiting_for_input_id
        global bot_status
        request_id = uuid.uuid4() 
        waiting_for_input_id = request_id  
        match bot_status:
            case 1:
                bot.register_next_step_handler(msg, add_task, call, request_id)
            case 2:
                bot.register_next_step_handler(msg, delete_task, call, *args, request_id)
            case 3:
                bot.register_next_step_handler(msg, change_task_status, call, *args, request_id)
            case _:
                return "Something went wrong"


    def send_message_and_delete_previous(chat_id, text, reply_markup=None):
        if chat_id in last_bot_message:
            try:
                bot.delete_message(chat_id, last_bot_message[chat_id])
            except Exception as e:
                print(f"Error deleting message: {e}")
        msg = bot.send_message(chat_id, text=text, reply_markup=reply_markup)
        last_bot_message[chat_id] = msg.message_id
        return msg


    @bot.callback_query_handler(func=lambda call: call.data == "veiw_routine_list")
    def view_routine_list(call):
        bot.answer_callback_query(call.id)
        routine_list = Activity.read(user_id=call.from_user.id)
        activities_list = [f"{i}. {item.routin} {(' ', '✅')[item.status]}" 
                           for i, item in enumerate(routine_list, start=1)]
        if routine_list:
            send_message_and_delete_previous(call.message.chat.id, "\n".join(activities_list))
        else:
            send_message_and_delete_previous(call.message.chat.id, no_routine_found_message)


    @bot.callback_query_handler(func=lambda call: call.data == "add_routin")
    def get_new_routine(call):
        global bot_status
        bot_status = 1
        bot.answer_callback_query(call.id)
        sent_msg = send_message_and_delete_previous(call.message.chat.id, prompt_add_message)
        bot_action(sent_msg, call)


    def add_task(message, call, request_id):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if request_id != waiting_for_input_id:
            return
        routine_list = Activity.read(user_id=message.from_user.id)
        if len(message.text) <= 30: 
            if message.text not in [item.routin for item in routine_list]:
                activity = Activity(routin=message.text, user_id=message.from_user.id)
                activity.save()
                send_message_and_delete_previous(call.message.chat.id, confirm_add_message)
            else:
                sent_msg = send_message_and_delete_previous(call.message.chat.id,
                                                duplicate_routine_error_message)
                bot_action(sent_msg, call)
        else:
            sent_msg = send_message_and_delete_previous(call.message.chat.id,long_error_message)
            bot_action(sent_msg, call)



    @bot.callback_query_handler(func=lambda call: call.data in ["routin_activities"])
    def routine_menu(call):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=routine_menu_message, reply_markup=routin_keyboard())


    @bot.callback_query_handler(func=lambda call: call.data == "remove_routin")
    def get_delete_task(call):
        global bot_status

        bot_status = 2
        bot.answer_callback_query(call.id)
        activities = Activity.read(call.from_user.id)
        routine_list = [f"{i}. {item.routin}" for i, item in enumerate(activities, start=1)]
        if routine_list:
            sent_msg = send_message_and_delete_previous(call.message.chat.id,
                                    prompt_delete_message + ":\n" + "\n".join(routine_list),
                                    reply_markup=delete_keyboard())
            bot_action(sent_msg, call, activities)
        else:
            send_message_and_delete_previous(call.message.chat.id, no_routine_found_message)


    def delete_task(message, call, activities, request_id):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if request_id != waiting_for_input_id:
            return 
        min_value, max_value = 1, len(activities)
        try:
            id_index = int(message.text) - 1
            if min_value <= id_index + 1 <= max_value:
                Activity.delete(activities[id_index].id)
                send_message_and_delete_previous(call.message.chat.id,confirm_delete_message)
            else:
                raise ValueError 
        except (IndexError, ValueError):
            sent_msg = send_message_and_delete_previous(
                call.message.chat.id, 
                f"لطفا یک عدد بین {min_value} تا {max_value} وارد کنید:")
            bot_action(sent_msg, call, activities)

    @bot.callback_query_handler(func=lambda call: call.data == "delet_all")
    def confirmation_delete_all(call):
        send_message_and_delete_previous(call.message.chat.id, confirm_delete_all_messages,
                                reply_markup=confirmation_keyboard())

    
    @bot.callback_query_handler(func=lambda call: call.data == "Yes")
    def delete_all(call):
        activities = Activity.read(call.from_user.id)
        for activitie in activities:
            Activity.delete(activitie.id)
        send_message_and_delete_previous(call.message.chat.id, delete_all_messages)
                            
        
    @bot.callback_query_handler(func=lambda call: call.data == "No")
    def cancel_delete_all(call):
        send_message_and_delete_previous(call.message.chat.id, cancel_delete_all_messages)
                            


    @bot.callback_query_handler(func=lambda call: call.data == "set_routine_status")
    def task_status(call):
        bot.answer_callback_query(call.id)
        activities = Activity.read(call.from_user.id)
        routine_list = [f"{i}. {item.routin}" for i, item in enumerate(activities, start=1)]
        if routine_list:
            sent_msg = send_message_and_delete_previous(call.message.chat.id,
                                    prompt_change_status_message + ":\n" + "\n".join(routine_list))
            bot_action(sent_msg, call, activities)
        else:
            send_message_and_delete_previous(call.message.chat.id, no_routine_found_message)


    def change_task_status(message, call, activities, request_id):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        global bot_status
        bot_status = 3
        if request_id != waiting_for_input_id:
            return  

        try:
            id_index = int(message.text) - 1
            if 0 <= id_index < len(activities):
                Activity.change_status(activities[id_index].id)
                bot.send_message(call.message.chat.id, text=confirm_change_status_message)
            else:
                raise IndexError
        except (IndexError, ValueError):
            sent_msg = bot.send_message(call.message.chat.id,
                                text=f"لطفا یک عدد بین 1 تا {len(activities)} وارد کنید:",
                                reply_markup=cancel_keyboard())
            bot_action(sent_msg, call, activities)


    task_thread = threading.Thread(target=unset_status)
    task_thread.start()
