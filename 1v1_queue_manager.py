import math
import os


class FIFO_Queue:

    def __init__(self):
        self.queue = []
        self.cache = []
        self.data = {}
        self.last_played = {}
        self.cache_size = 1

    # Adds a name to the queue, increases cache size
    def add(self, name: str):
        if len(self.queue) > 1:
            self.balance_cache(name)
            self.cache_size += len(self.queue)

        self.queue.append(name)
        self.last_played[name] = ""

    # Balances the cache if there is enough progress
    # in the cache
    def balance_cache(self, name: str):
        if len(self.cache) >= math.ceil(len(self.queue) / 2) and len(self.queue) > 1:
            cache_completion = 1.0 * len(self.cache) / self.cache_size
            game_count = math.floor(1.0 * cache_completion * len(self.queue))

            for i in range(len(self.queue) - 1, len(self.queue) - game_count - 1, -1):
                self.cache.append(self.matchup_string(name, self.queue[i]))

    # Removes a name from queue and all related cache entries
    def remove(self, name: str):
        self.queue.remove(name)

        if len(self.queue) > 1:
            self.cache_size -= len(self.queue)

        tmp_list = []
        for i in range(len(self.queue)):
            tmp_list.append(self.matchup_string(name, self.queue[i]))

        for item in tmp_list:
            if item in self.cache:
                self.cache.remove(item)

    # Easy way to represent matchups as strings
    def matchup_string(self, p1: str, p2: str):
        if p1 < p2:
            return p1 + p2
        else:
            return p2 + p1

    # determine the next 2 players by iterating over the queue,
    # checking to see if each matchup exists in the cache, and
    # picking the first possible combination of players not in
    # the cache
    def get_next(self):

        if len(self.queue) < 2:
            return ("INVALID", "INVALID")

        elif len(self.queue) >= 2:
            p1_index: int = 999
            p2_index: int = 999
            is_not_last_played = False

            if len(self.cache) == self.cache_size:
                self.cache.clear()

            for i in range(len(self.queue) - 1):
                for j in range(i + 1, len(self.queue)):
                    is_not_last_played = (
                        self.last_played[self.queue[i]] != self.queue[j]
                        and self.last_played[self.queue[j]] != self.queue[i]
                    )
                    if self.matchup_string(
                        self.queue[i], self.queue[j]
                    ) not in self.cache and (is_not_last_played or len(self.queue) < 3):
                        p1_index = i
                        p2_index = j
                        break
                if p1_index != 999:
                    break

            p2: str = self.queue.pop(p2_index)
            p1: str = self.queue.pop(p1_index)
            self.last_played[p1] = p2
            self.last_played[p2] = p1

            self.queue.append(p1)
            self.queue.append(p2)
            self.cache.append(self.matchup_string(p1, p2))
            return (p1, p2)

        else:
            return ("INVALID", "INVALID")

    def str_queue(self):
        return str(self.queue)

    def str_cache(self):
        return str(self.cache) + " cache capacity: " + str(self.cache_size)

    def sim(self, num: int):
        for i in range(num):
            for j in range(num - 1):
                print(str(num) + str(num))


if __name__ == "__main__":

    queue = FIFO_Queue()

    clear = lambda: os.system("cls")

    print("\n  1v1 Queue Manager  ")
    print("=====================")
    print("a [name] or add [name] - Adds given name to end of queue")
    print("r [name] or remove [name] - Removes given name from queue")
    print("n or next - Returns first 2 players in queue")
    print("v or view - Returns the full queue, with the left side being the 'front'")
    print("c or cache - Displays the current cache list")
    print("s or sim - For testing purposes, shows results for a specified lobby size")
    print("h or help - Displays commands")
    print("q or quit - Quit\n")

    while True:

        userInput = str(input("> "))

        if userInput.split()[0] == "help" or userInput.split()[0] == "h":
            clear()
            print("\na [name] or add [name] - Adds given name to end of queue")
            print("r [name] or remove [name] - Removes given name from queue")
            print("n or next - Returns first 2 players in queue")
            print(
                "v or view - Returns the full queue, with the left side being the 'front'"
            )
            print("c or cache - Displays the current cache list")
            print(
                "s or sim - For testing purposes, shows results for a specified lobby size"
            )
            print("h or help - Displays commands")
            print("q or quit - Quit\n")

        elif userInput.split()[0] == "add" or userInput.split()[0] == "a":
            clear()
            queue.add(userInput.split()[1])
            print("\n" + userInput.split()[1] + " added.\n")

        elif userInput.split()[0] == "remove" or userInput.split()[0] == "r":
            clear()
            try:
                queue.remove(userInput.split()[1])
                print("\n" + userInput.split()[1] + " removed.\n")
            except:
                print("\nPlayer not in queue.\n")

        elif userInput == "next" or userInput == "n":
            clear()
            next_round = queue.get_next()
            if next_round[0] != next_round[1]:
                print("\n" + str(next_round) + "\n")
            else:
                print("\nNot enough players to start a match.\n")

        elif userInput == "view" or userInput == "v":
            clear()
            print("\n" + queue.str_queue() + "\n")

        # For debug purposes, this option isn't expressed to the user
        elif userInput == "cache" or userInput == "c":
            clear()
            print("\n" + queue.str_cache() + "\n")

        # For debug purposes, this option isn't expressed to the user
        elif userInput == "sim" or userInput == "s":
            clear()
            print("Input a lobby size to simulate and number of simulation rounds.")
            print("2520 is a good simulation round number for 2-9 player lobbies.")
            print("The left column contains a number representative of 2 players")
            print("(i.e. '14' is 'player 1 vs player 4'). The right column is the")
            print(
                "total number of times that particular matchup was played in the sim."
            )
            num = int(input("\nSimulated Lobby Size: "))
            # 2520 is a good default for 2-9 player lobbies
            rounds = int(input("Number of simulation rounds: "))
            simQueue = FIFO_Queue()

            for i in range(num):
                simQueue.add(str(i + 1))

            for i in range(num - 1):
                for j in range(i + 1, num):
                    data_string = (
                        sorted(str(i + 1) + str(j + 1))[0]
                        + sorted(str(i + 1) + str(j + 1))[1]
                    )
                    simQueue.data[data_string] = 0

            for i in range(rounds):
                tup = simQueue.get_next()
                game: str = tup[0] + tup[1]
                dat = str(sorted(game)[0]) + str(sorted(game)[1])
                simQueue.data[dat] += 1

            for x, y in simQueue.data.items():
                print(x, y)
            print()

        elif userInput == "q" or userInput == "quit":
            break

        else:
            pass
