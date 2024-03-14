import json, requests, random, time, dotenv

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n) : ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        


HOST = "imdb8.p.rapidapi.com"
KEY = dotenv.dotenv_values('./keys.env').get('IMDB_API_KEY')
url = "https://imdb8.p.rapidapi.com/title/find"
bad_file = str(".\BAD.txt")
movies_file = str(".\MOVIES.txt")

do = 0
random.seed(time.process_time())

headers = {
    'x-rapidapi-host': HOST,
    'x-rapidapi-key': KEY,
    'content-type': "application/json"
    }

if __name__ == "__main__":
  
  while do != 6:
    try:
      do = int(input("\nWhat would you like to do ?\n 1/ Add a movie\n 2/ Remove a movie\n 3/ Create the Poll command\n 4/ List the movies in the database\n 5/ <sad naruto theme playing>\n 6/ Exit\n> "))
      i = 0
      search = ""
      dup = ""
      found = False
      exist = False
      movies = []
      choices = []

      if do == 1:
        index = 0
        search = str(input("\nEnter the movie name to search ('c' to cancel): "))
        #search = open(str("G:\Mon Drive\Codes\Autres\IMDB\message.txt")).read() #

        if search == "c":
          movies = []
          continue

        print("Finding matches for " + search + "...  \n")
        movielist = search.splitlines() #

        for search in movielist: #
          index = 0
          querystring = {"q":search}
          time.sleep(1)
          response = requests.request("GET", url, headers=headers, params=querystring)

          #print(json.loads(response.text))

          if(response.status_code == 200):
              data = json.loads(response.text)

              #print(json.dumps(data, indent=4, sort_keys=True))
              #wait = input()

              results = data["results"]

              for x in results:

                  movie_id = x["id"]  
                  if not movie_id.startswith("/title/"):
                      continue
                  
                  try:
                    movie_title = x["title"]
                    movie_year = str(x["year"])
                    #movie_actor = str(x["principals"]["name"])

                    if index < 10: # 1
                      print(" " + str(index+1) + "/")
                      print("Movie:\t" + movie_title + " (" + movie_year + ")")
                      print("URL:\thttps://www.imdb.com" + movie_id)
                      print("\n")

                      movies.append(movie_title + " (" + movie_year + ") : https://www.imdb.com" + movie_id)
                    index+=1

                  except Exception:
                    continue

              correct = int(input("Select the desired movie ('0' to cancel): "))

              if correct == 0:
                movies = []
                continue

              file = open(movies_file)
              lines = file.read().splitlines()
              if lines.count(movies[correct-1]) == 0:
                lines.append(movies[correct-1])
              file.close()
              file = open(movies_file, "w")
              for x in lines:
                file.write(x + "\n")
              file.close()

              with open(movies_file, 'r') as file:
                lines = file.readlines()
                unique_lines = list(set(lines))

              with open(movies_file, 'w') as file:
                file.writelines(unique_lines)

              print(movies[correct-1] + " added !")
              movies = []

          else:
              print("Invalid request or error in response")

      if do == 2:
        file = open(movies_file)
        lines = file.read().splitlines()
        file.close()

        rm = str(input("\nSearch for the movie to remove : "))

        for i in lines:
              if rm in i:
                  print(i)
                  if yes_or_no("Remove ?"):
                    lines.remove(i)
                  found = True
        if not found:
          print("No such movie")

        file = open(bad_file)
        lines2 = file.read().splitlines()
        file.close()

        for i in lines2:
              if rm in i:
                  lines2.remove(i)

        found = False

        file = open(movies_file, "w")
        for x in lines:
            file.write(x + "\n")
        file.close()

        file = open(bad_file, "w")
        for x in lines2:
            file.write(x + "\n")
        file.close()

        with open(movies_file, 'r') as file:
          lines = file.readlines()
          unique_lines = list(set(lines))

        with open(movies_file, 'w') as file:
          file.writelines(unique_lines)        

      if do == 3:
        row = 0

        file = open(movies_file)
        lines = file.read().splitlines()
        file.close()

        while row <= 10:
          chosen_row = random.choice(lines)
          choices.append(chosen_row)
          lines.remove(chosen_row)
          row+=1

        print("\n/poll question:Quel film pour la prochaine séance ? choice_a:"+str(choices[0])+" choice_b:"+str(choices[1])+" choice_c:"+str(choices[2])+" choice_d:"+str(choices[3])+" choice_e:"+str(choices[4])+" choice_f:"+str(choices[5])+" choice_g:"+str(choices[6])+" choice_h:"+str(choices[7])+" choice_i:"+str(choices[8])+" choice_j:"+str(choices[9]))

      if do == 4:
        file = open(movies_file)
        lines = file.read().splitlines()
        file.close()

        print("")
        for l in lines:
          l = l[:-40]
          l = "- " + l
          print(l)
        print("\nNombre de films: " + str(len(lines)) + "\n")

      if do == 5:
        file = open(movies_file)
        lines = file.read().splitlines()
        file.close()

        file = open(bad_file)
        lines2 = file.read().splitlines()
        file.close()

        if not lines2 :
          print("\nNo bad movies")
        else :
          for l in lines2:
            print(l)
        print("")

        bad = str(input("A movie you don't like ? ('c' to cancel) "))

        if bad == "c":
          lines2 = []
          lines = []
          continue

        print("")
        for j in lines:
            if bad in j:
                print(j)
                if yes_or_no("This one ?"):
                  found = True
                  if lines2.count(j) >= 1:
                    dup = lines2.index(j)
                    exist = True
                  else:
                    lines2.append(j)
                    exist = False
                  break
        if not found:
          print("No such movie")

        found = False

        file = open(bad_file, "w")
        for x in lines2:
          if exist and lines2.index(x) == dup:
            file.write("TIME TO GO: " + x + "\n")
          else:
            file.write(x + "\n")
        file.close()

        with open(movies_file, 'r') as file:
          lines = file.readlines()
          unique_lines = list(set(lines))

        with open(movies_file, 'w') as file:
          file.writelines(unique_lines)        

      if do != 6 : time.sleep(1)

    except Exception as e:
      print("\nError: " + str(e))
      continue