# Payments

Types:

```python
from mpesaflow.types import Payment
```

Methods:

- <code title="post /paybill">client.payments.<a href="./src/mpesaflow/resources/payments.py">create</a>(\*\*<a href="src/mpesaflow/types/payment_create_params.py">params</a>) -> <a href="./src/mpesaflow/types/payment.py">Payment</a></code>

# Transactions

Types:

```python
from mpesaflow.types import TransactionStatus
```

Methods:

- <code title="get /transaction-status/{transactionId}">client.transactions.<a href="./src/mpesaflow/resources/transactions.py">retrieve</a>(transaction_id) -> <a href="./src/mpesaflow/types/transaction_status.py">TransactionStatus</a></code>
