# Devoted Health Code Screen
![Every Readme needs a fun header image. It's the law.](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)

## Introduction
This is a basic in-memory database per spec, programmed in Python 3.

## Notes on design and tradeoffs
### Adding a second dictionary to track value counts increases the use of resources
This is true! Since all of the data storage is in-memory, whenever we add a distinct value it is going to increase the resources needed by `value_counter`. However, I felt that this was a good tradeoff versus iterating through all of the values in the database because it reduces the time of the `COUNT` function from O(n) to O(1). We're sacrificing memory for speed which is a consideration for all code. I'll be happy to discuss the trade-off during review. 

### Using a transaction log vs. copying the entire database to a temporary dictionary
My original approach to this problem was to simply copy the entire contents of the `db` and `value_counter` into a new array as temporary storage while the transaction changes occurred. Then if we needed a rollback we could just copy those original arrays back over. However in "Performance Requirements" memory usage was specifically highlighted as a concern. This altered my approach to use a log of change sets instead. I actually like the brute force approach of copying the database as it is much less complex and also provides the ability to do nested transactions, but I ultimately went with the more memory efficient solution. I'm also happy to discuss this during review.

## How To Operate
### Starting The Program
You can start the program locally:

```python database.py```

Or, you can use the provided Dockerfile (Bonus: it'll also run the tests for you!):

```
docker build --no-cache . -t devoted-screen
docker run -it devoted-screen
```

### Functions
#### SET [name] [value]
Sets the name in the database to the given value

#### GET [name]
Prints the value for the given name. If the value is not in the database, prints N​ULL

#### DELETE [name]
Deletes the value from the database

#### COUNT [value]
Returns the number of names that have the given value assigned to them. If that value is not assigned anywhere, prints ​0

#### END
Exits the database

#### BEGIN
Begins a new transaction

#### ROLLBACK
Rolls back the most recent transaction. If there is no transaction to rollback, prints TRANSACTION NOT FOUND

#### COMMIT
Commits a​ll​ of the open transactions

### Example Commands
Enter commands from the spec into STDIN. Here are some examples:

*(Note: The key and value will only accept strings with no spaces in them)*

```
>> SET name Griffin
>> GET name
>> Griffin
>> COUNT Griffin
>> 1
>> DELETE name
>> GET name
>> NULL
```

To exit the program, use `END`.

#### Transactions
You can also use a transaction. A transaction log will be kept in `transaction_logs` and applied using the command `COMMIT` or discarded with `ROLLBACK`.

```
>> SET name Griffin
>> BEGIN
>> SET name Daphne
>> GET name
>> Daphne
>> ROLLBACK
>> Get name
>> Griffin
```

## How To Test
Unit tests are included. You can run them using `pytest`.

```pytest tests.py```