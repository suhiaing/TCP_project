import socket
import json
import random

class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9998
        self.input_checking(sms)

    def client_runner(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client  # to send and received data

    def input_checking(self, sms):
        if sms == "gad":
            self.get_all_data(sms)

        elif sms == "login":
            self.login(sms)

        elif sms == "reg":
            self.register(sms)
        else:
            print("Invalid Option")


    def login(self, info):
        try:
            print("############################ This is login Form #########################")
            l_email = input("Enter your email to login:")
            l_pass = input("Enter your password to login:")

            client = self.client_runner()
            sms = info + ' ' + l_email + ' ' + l_pass  # login email password
            sms = bytes(sms, "utf-8")
            client.send(sms)
            received_from_server = client.recv(4096)
            user_info: dict = json.loads(received_from_server.decode("utf-8"))
            self.option_choice(user_info, client)


        except Exception as err:
            print(err)

    def option_choice(self, user_info, client):
        print("################################ user option #################################")
        print("Email :", user_info["email"])
        print("Info :", user_info["info"])
        print("Point :", user_info["point"])

        try:
            option = input("Press 1 to Get User Option:\nPress 2 To Get Main Option:\nPress 3 To Exit:")
            if option == '1':
                self.user_option(user_info, client)
            elif option == '2':
                self.input_checking("from_option")  # to write more option
            elif option == '3':
                exit(1)
            else:
                print("Invalid Option [X]")
                self.option_choice(user_info, client)

        except Exception as err:
            print(err)

    def user_option(self, user_info, client):
        print("################################ user option ################################")
        try:
            option = input("Press 1 To Vote:\nPress 2 to get more points:\nPress 3 to Transfer Point:\n"
                           "Press 4 To get Voting Ranking:\nPress 5 to change user information \nPress 6 to Delete Acc:\nPress 7 "
                           "to Exit:")

            if option == '1':
                self.voting(user_info)

            else:
                print("Invalid option")
                self.user_option(user_info, client)

        except Exception as err:
            print(err)
            self.user_option(user_info, client)

    def voting(self, user_info):
        print("################################ voting #########################")
        client = self.client_runner()
        sms = bytes("candidate_info", "utf-8")
        client.send(sms)

        info = client.recv(4096)
        candi_info = json.loads(info.decode("utf-8"))
        print(candi_info)  
        print(type(candi_info))
        for i in candi_info:
            print("No: ",i,"Name: ",candi_info[i]["name"],"Point",candi_info[i]["vote_point"])

        client.close()

    def get_all_data(self, sms):
        print("################################## getting all data #################################")
        client = self.client_runner()
        sms = bytes(sms + ' ', "utf-8")
        client.send(sms)
        received_from_server = client.recv(4096)
        # print(received_from_server.decode("utf-8"))

        dict_data: dict = json.loads(received_from_server.decode("utf-8"))
        print(type(dict_data))
        print(dict_data)
        client.close()

    def register(self, sms):
        print("################################ register #########################")
        client = self.client_runner()
        sms = bytes(sms + ' ',"utf-8")
        client.send(sms)
        r_id = random.randint(10, 10000)
        r_email:str = input("Please enter your email address: ")
        r_password:str = input("Please enter your password: ")
        r_phone:int = input("Please enter your phone number: ")
        r_point:int = 100
        info:str = "User data is"+r_email+"id : "+str(r_id)
        data_form = {"_id": r_id, "email": r_email, "password": r_password, "phone": r_phone,"info":info,"point":r_point}
        r_form = json.dumps(data_form)
        r_form_bytes = bytes(r_form,"utf-8")
        client.send(r_form_bytes)   
        print("SENDING TO SERVER:PLEASE WAIT FOR A SECOND")
        server_reply = client.recv(1024)
        print(server_reply.decode("utf-8"))
        client.close()

if __name__ == "__main__":
    while True:
        print("################################ main function #########################")
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)