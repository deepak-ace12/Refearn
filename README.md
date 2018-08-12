### Running The Project

1. Install the dependencies from requirement.txt
```
pip install -r project/requirement.txt
```
2. Go to the directory /project and run the following command
```
python manage.py migrate
python manage.py runserver
```

Functionalities :
1. Add Customer

```
go to link http://127.0.0.1:8000/api/customer/

Add the details of the customer in the form at the bottom of the page
```

2. Get Customer By Id
```
go to link http://127.0.0.1:8000/api/customer/CUSTOMER_ID

where customer_id is an id of any customer.
```

3. Add Referral
```
go to the link http://127.0.0.1:8000/api/add/refferal/

add customer id and the id and referral id.
Referral Id is the id of the customer who is referring the new customer.
```

4.Fetch All Children
```
go to the link http://127.0.0.1:8000/api/customer/CUSTOMER_ID/children/

It will fetch all the customers who has referral of given CUSTOMER_ID
```

5. Fetch All Customers With Referral Count
```
go to the link http://127.0.0.1:8000/api/refferal/

it will give the list of all customers with decreasing order of number of referrals of children
```

6. Add Ambassador:
```
go to the link http://127.0.0.1:8000/api/add/ambassador/

it will open an html form which will have 3 fields:
  a. email_id
  b. date of joining
  c. referral_id
by default the customer being added will be an ambassador
```

7. Convert Customer To Ambassador
```
go to link http://127.0.0.1:8000/api/customer/CUSTOMER_ID
and check the field "is_ambassador"
the customer will be converted to an ambassador
```

8. Fetch All Ambassador Children
```
go to the link http://127.0.0.1:8000/api/customer/ambassador/CUSTOMER_ID/

It will give the list of all the children of an ambassador at all level. 
It will go upto the last node of the tree
```

9. Fetch Children At Nth Level
```
go to the link http://127.0.0.1:8000/api/customer/ambassador/CUSTOMER_ID/LEVEL/

LEVEL is an int >=1

it will return the list of children at given level.
```




