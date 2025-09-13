import grpc
from concurrent import futures
import users_pb2
import users_pb2_grpc

class UserService(users_pb2_grpc.UserServicer):

    def __init__(self):
        self.users=[
            {"id":1,"name":"John Doe","email":"john.doe@email.com"},
            {"id":2,"name":"Joe Smith","email":"joe@email.com"}
        ]


    def CreateUser(self, request, context):
        new_user = {
            "id" : self.users[len(self.users)-1]["id"]+1,
            "name" : request.name,
            "email":request.email,
        }
        self.users.append(new_user)
        return users_pb2.UserResponse(
            id = new_user["id"],
            name = new_user["name"],
            email= new_user["email"]
        )
    
    def GetUser(self, request, context):
        id = request.id
        user = next((u for u in self.users if u["id"]==id),None)
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.UserResponse()
        return users_pb2.UserResponse(
            id = user["id"],
            name= user["name"],
            email=user["email"]            
        )
    
    def ListUsers(self, request, context):
        users=[];
        for user in self.users:
            users.append(users_pb2.UserResponse(
                id = user["id"],
                name = user["name"],
                email = user["email"]
            ))
        return users_pb2.UserListResponse(users=users)
    
    def EditUser(self, request, context):
        id = request.id
        edit_user = next((u for u in self.users if u["id"]==id),None)
        if edit_user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return users_pb2.UserResponse
        edit_user["name"] = request.name
        edit_user["email"] = request.email
        return users_pb2.UserResponse(
            id=edit_user["id"],
            name=edit_user["name"],
            email=edit_user["email"]
        )
    
    def DeleteUser(self, request, context):
        id = request.id
        index = next((i for i,u in self.users if u["id"]==id),None)
        if index is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User Not found")
            return ()
        self.users = [u for u in self.users if u["id"]!=id]
        return()
    
def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        users_pb2_grpc.add_UserServicer_to_server(UserService(),server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("grpc Server Started on port 50001")
        server.wait_for_termination()

if __name__=='__main__':
    serve()
    

    