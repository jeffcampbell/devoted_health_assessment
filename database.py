import sys

class Database:
    # Initialize our three arrays: db is the main database, transaction_logs will track changes when a transaction is open, value_counter will track the count of distinct values in db.
    def __init__(self):
        self.db = {}
        self.transaction_logs = []
        self.value_counter = {}

    def set(self, key, value):
        if self.transaction_logs:
            self.record_change(key)
        if key in self.db:
            self.decrement(self.db[key])
        self.db[key] = value
        self.increment(value)

    def get(self, key):
        return self.db.get(key, "NULL")

    def delete(self, key):
        if key in self.db:
            if self.transaction_logs:
                self.record_change(key, deleted=True)
            self.decrement(self.db[key])
            del self.db[key]

    def count(self, value):
        return self.value_counter.get(value, 0)

    def begin(self):
        self.transaction_logs.append({})

    def commit(self):
        if self.transaction_logs:
            self.transaction_logs.pop()

    # This is definitely the most complex piece of code. It needs to work through the transaction logs to find all of the changed keys and revert the changes. It also has to do this with the value_counter without something getting out of state (there's a unit test to check for this).
    def rollback(self):
        if not self.transaction_logs:
            return "TRANSACTION NOT FOUND"
        last_changes = self.transaction_logs.pop()
        for key, (old_value, deleted) in last_changes.items():
            current_value = self.db.get(key)
            if deleted:
                if old_value is not None:
                    self.db[key] = old_value
                    self.increment(old_value)
            else:
                self.decrement(current_value)
                if old_value is not None:
                    self.db[key] = old_value
                    self.increment(old_value)
                else:
                    del self.db[key]

    def record_change(self, key, deleted=False):
        if self.transaction_logs:
            last_transaction = self.transaction_logs[-1]
            if key not in last_transaction:
                last_transaction[key] = (self.db.get(key), deleted)

    def increment(self, value):
        if value in self.value_counter:
            self.value_counter[value] += 1
        else:
            self.value_counter[value] = 1

    def decrement(self, value):
        if value in self.value_counter:
            if self.value_counter[value] == 1:
                del self.value_counter[value]
            else:
                self.value_counter[value] -= 1

def main():
    db = Database()
    # I'm putting this in a while loop which is a little risky but I like it for running a small application like this. It also lets me decorate the STDIN with the ">>" to make things more legible.
    while True:
        print(">> ", end='', flush=True)

        line = sys.stdin.readline()
        if not line or line.strip() == "END":
            break

        try:
            # A tidy little piece of boilerplate for parsing commands with args.
            raw_command = line.strip().split()
            command = raw_command[0]
            args = raw_command[1:]

            if len(args) > 2:
                print("Too many arguments.")
            elif command == "SET":
                db.set(*args)
            elif command == "GET":
                result = db.get(*args)
                print(result if result is not None else "NULL")
            elif command == "DELETE":
                db.delete(*args)
            elif command == "COUNT":
                result = db.count(*args)
                print(result)
            elif command == "BEGIN":
                db.begin()
            elif command == "ROLLBACK":
                result = db.rollback()
                if result:
                    print(result)
            elif command == "COMMIT":
                db.commit()
            else:
                print(f"I don't understand the command: {line.strip()}. Please refer to the readme for command structure.")
        except Exception as e:
            # It's always nice to have a polite error message.
            print(f"Error: {str(e)}. Please refer to the readme for command structure.")

if __name__ == "__main__":
    main()
