from Routine.routine_markup import *
from routine_config import *
from Routine.routine_models import Activity
import threading
import datetime
from time import sleep



def unset_status():
    while True:
        now_time = datetime.datetime.now()
        time = now_time.strftime("%H:%M")
        if time == "19:02":
            Activity.reset_all_status()
        sleep(60)

class RoutineHandler:

    def __init__(self, bot) -> None:
        self.bot = bot

    def hande_routine_menu(self):
        self.bot.callback_query_handler(func=lambda call: call.data=="routin_activities")
        @self.bot.callback_query_handler(func=lambda call: call.data=="back_to_routine_menu")
        def routin_menu(call):
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text_2, reply_markup=routin_keyboard())
    

    def hande_new_task(self):
                
        @self.bot.callback_query_handler(func=lambda call: call.data=="add_routin")
        def get_new_routin(call):
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                            text=text_3, reply_markup=comeback_routin_keyboard())  
            self.bot.register_next_step_handler(call.message, add_task )


        def add_task(message):
            routin_list = Activity.read(message.from_user.id)
            activities_list = [item.routin for item in routin_list]
            if message.text not in activities_list:
                activity = Activity(routin=message.text, user_id=message.from_user.id)
                activity.save()
                self.bot.send_message(message.chat.id, "فعالیت شما با موفقیت اضافه شد.")
            else:
                self.bot.send_message(message.chat.id,
                                " این فعالیت  تکراری است. لطفا یک فعالیت جدید وارد کنید:")
                self.bot.register_next_step_handler(message, add_task)

    def handel_back_to_main(self):
        @self.bot.callback_query_handler(func=lambda call: call.data=="back_to_main")
        def back_to_main(call):
                self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text_1, reply_markup=main_keyboard())

    def handel_veiw_list(self):
        @self.bot.callback_query_handler(func=lambda call: call.data=="veiw_routine_list")
        def veiw_routin_list(call):
            routin_list = Activity("sqlite:///data230.db").read(user_id=call.from_user.id )
            activities_list = [f"{i}. {item.routin}{(' ', '✅')[item.status]}" for i,
                            item in enumerate(routin_list, start=1)]
            self.bot.send_message(chat_id=call.message.chat.id, text="\n".join(i for i in activities_list))

    def handel_delet_task(self):
        @self.bot.callback_query_handler(func=lambda call: call.data=="remove_routin")
        def get_delete_task(call) :
            activities_list = Activity("sqlite:///data230.db").read(call.from_user.id)
            routin_list = [f"{i}. {item.routin}" for i, item in enumerate(activities_list, start=1)]
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="شماره فعالیتی که می‌خوای حذف کنی وارد کن"
                                +":\n\n" + "\n ".join(i for i in routin_list),
                                reply_markup=comeback_routin_keyboard())
            self.bot.register_next_step_handler(call.message, delet_task, activities_list=activities_list )


        def delet_task(message, activities_list):
            try:
                id_index = int(message.text)-1
                if id_index >= 0:
                    id = activities_list[id_index].id
                    Activity.delete(id)
                    self.bot.send_message(message.chat.id, "فعالیت شما با موفقیت حذف شد.")
                elif id_index < 0:
                    self.bot.send_message(message.chat.id,
                                    text=f"لطفا یک عدد بین 1 تا {len(activities_list)}وارد کنید :")
                    self.bot.register_next_step_handler(message, delet_task, activities_list=activities_list)
            except IndexError:
                self.bot.send_message(message.chat.id,
                                text=f"لطفا یک عدد بین 1 تا {len(activities_list )}وارد کنید:")
                self.bot.register_next_step_handler(message, delet_task, activities_list=activities_list)
            except ValueError:
                self.bot.send_message(message.chat.id, text="لطفا یک عدد صحیح وارد کنید:")
                self.bot.register_next_step_handler(message, delet_task, activities_list=activities_list)

    def handel_task_status(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == "set_routine_status")
        def task_status(call):
            activities_list = Activity.read(call.from_user.id)
            routin_list = [f"{i}. {item.routin}" for i, item in enumerate(activities_list, start=1)]
            self.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text= "شماره فعالیتی که می‌خوای تیک بزنی وارد کن"+":\n\n" 
                                + "\n ".join(i for i in routin_list),reply_markup=comeback_routin_keyboard())
            self.bot.register_next_step_handler(call.message, change_task_status, activities_list=activities_list)
        
            
        def change_task_status(message, activities_list):
            try:
                id_index = int(message.text)-1
                id = activities_list[id_index].id
                if  activities_list[id_index].status == 0 and id_index >= 0:
                    Activity.change_status(id)
                    self.bot.send_message(message.chat.id, "فعالیت شما با موفقیت تیک خورد.")
                    self.bot.register_next_step_handler(message, change_task_status, activities_list)
                elif id_index < 0:
                    self.bot.send_message(message.chat.id,
                                    text=f"لطفا یک عدد بین 1 تا {len(activities_list)}وارد کنید:")
                    self.bot.register_next_step_handler(message, change_task_status, activities_list)
                else:
                    self.bot.send_message(message.chat.id, "این فعالیت قبلا تیک خورده.")
            except IndexError:
                self.bot.send_message(message.chat.id,
                                text=f"لطفا یک عدد بین 1 تا {len(activities_list)} وارد کنید:")
                self.bot.register_next_step_handler(message, change_task_status, activities_list)
            except ValueError:
                self.bot.send_message(message.chat.id, text="لطفا یک عدد صحیح وارد کنید:")
                self.bot.register_next_step_handler(message, change_task_status, activities_list)

task_1 = threading.Thread(target=unset_status)
task_1.start()