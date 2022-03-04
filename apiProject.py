import requests, json, os
DUMP = 'C:\\Users\\jacob\\Desktop\\cw_temp.txt'
USERNAMES = 'C:\\Users\\jacob\\Desktop\\cw_usernames.txt'
CHALLENGES = 'C:\\Users\\jacob\\Desktop\\cw_challenges.txt'
SNACKS = 'C:\\Users\\jacob\\Desktop\\cw_snacks.txt'
LOG = 'C:\\Users\\jacob\\Desktop\\cw_log.txt'
#d = open("C:\\Users\\jacob\\Desktop\\old_scores.txt","r+")

def build_list(file):
    users = []
    # Getting the users from the USERNAMES file.txt file.
    # The user name must be there in order to be checked.
    with open(file,'r') as f:
        for line in f.readlines():
            users.append(line.strip())
    return users


def get_completed(file,log,user_list):
    # Uses the codewars API to get the number of completed challenges of each user in the given list.
    # Builds a dictionary with the key being the user name and the value being the number of completed challenges

    user_dict = {}
    errors = []
    for user in user_list:
        user = user.strip()
        req ="https://www.codewars.com/api/v1/users/" + user
        #print(req)
        response = requests.get(req)
        print(f"user: {user} -- {response.status_code}")
        if response.status_code > 202:
            with open(log,'w') as log:
                log.write(str(response.status_code)+ "--"+ user)
                errors.append(user)
                continue
        lib = response.json()
        test = json.dumps(lib,sort_keys=True,indent=4)
        #cw_path = 'C:\\Users\\jacob\\Desktop\\cwhonor.txt'
        f = open(file,'w')
        f.write(test)
        f.close()
        f = open(file,'r')
        for line in f.readlines():
            if "totalCompleted" in line:
                #print(line[26:])
                completed = line[26:]
                completed = completed.strip()
                break
            else:
                #print("No challenge found")
                completed = 404
        f.close()
        user_dict[user] = completed
        os.remove(file)
    return user_dict, errors

def check_completed(challenges_file,snack_file,user_dict,user_list):
    # Checks to see if each user in user_dict has completed a challenge
    ref_dict = {}
    with open(challenges_file,'r') as f:
        for line in f.readlines():
            line = line.strip()
            line_list = line.split(',')
            line_list.pop(-1)
            #print(f"line_list: {line_list}")
            for each in line_list:
                user_bundle = each.split()
                #print(f"user_bundle: {user_bundle}")
                user = user_bundle[0]
                challenge = user_bundle[1]
                #print(f'user: {user}')
                #print(f"challenge: {challenge}")
                ref_dict[user] = challenge
    #print(ref_dict)
    with open(snack_file,'w') as f:
        for user in ref_dict:
            for u in user_dict:
                if user == u:
                    #print(f"user: {user}")
                    #print(f'ref_dict[user]: {ref_dict[user]}')
                    #print(f'user_dict[u]: {user_dict[u]}')
                    if int(ref_dict[user]) < int(user_dict[u]):
                        message = str.format("{:<25.25}:  {:>9}{}",u,"Snacks = ","True\n\n")
                        #f.write(u+": \t\tSnacks = True\n")
                        f.write(message)
                    elif int(ref_dict[user]) >= int(user_dict[u]):
                        message = str.format("{:<25.25}:  {:>9}{}",u,"Snacks = ","False\n\n")
                        #f.write(u+": \t\tSnacks = False\n")
                        f.write(message)
                    else:
                        message = str.format("{:<25.25}:  {:>9}{}",u,"Snacks = ","404\n\n")
                        #f.write(u+": \t\t404\n")
                        f.write(message)



def update_member_file(file,user_dict):
    # Updates the file containing the members with the number of completed challenges so that it can be checked next week.
    with open(file,'w') as f:
        for user in user_dict:
            f.write(user+" "+str(user_dict[user])+",")


users = build_list(USERNAMES)
user_dict, errors = get_completed(DUMP,LOG,users)
check_completed(CHALLENGES,SNACKS,user_dict,users)
update_member_file(CHALLENGES,user_dict)
if len(errors) > 0:
    print(f"The following users had errors: {errors}\nCheck the cw_log.txt file for more.")
    input("Press enter to continue")
else:
    print(f"There were no issues check the cw_snacks.txt file to see who gets snacks!")
    input("Press enter to continue")