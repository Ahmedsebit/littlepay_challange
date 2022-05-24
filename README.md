# littlepay_challange

# Assumptions
- The tap ON/OFF in a csv are from the same device, hence also from the same bus with the same bus_id
- A user can use the same bus during the day so the can have mmultiple taps ON/OFF in the same device 


## Installation
- Clone repository `git clone https://github.com/Ahmedsebit/littlepay_challange.git`
- Install virtualenv `pip install virtualenv`
- Create environment `virtualenv --python=python3 env`
- Activate environment `source env/bin.activate`
- Install requirments `pip install -r requirements.txt`
- create a .env file
- add enviroment variable to .env file
- - STOP1_TO_STOP2="$ 3.25"
- - STOP2_TO_STOP3="$ 5.50"
- - STOP1_TO_STOP3="$ 7.30"
- run application `flask run`


## Testing
- Run tests using `coverage run -m nose`
- To get the coverage `coverage report -m`

## Doc
- http://localhost:5000/apidocs/#/

## APIs
- http://127.0.0.1:5000/api/pectus_finance/expenses
- http://127.0.0.1:5000/api/pectus_finance/aggregates
