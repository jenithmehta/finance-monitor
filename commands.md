Q. what is **repr**()?

> it is function defined in a class which is string representation of that class and its arguments
> eval is used to parse this string and later re-recreate the same instance of an object.
> b = test_class()
> same_instance = eval(b.**repr**())
> b == same_instance -> True

<h4>T. Create intance of db, add statements object, and try out queries:  </h4>

Q. what is **uuid**?

> uuid is a sequence of hexadecimal characters
> it is made to uniquely identify object in code
> it is made out of timestamp and mac address
> hexadecimal characters are numberic+alphabetic representation of bits. 1 byte = 2 hex chracters

Q. what is all() method in **sqlalchemy**?

> all() gives the result as a list
> all is memory intensive
> query object is iterative
> for group by operations one() or first() can be used
> if more results are expected, just loop through the results to avoid memory surge
