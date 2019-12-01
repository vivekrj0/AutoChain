# AutoChain
**A decentralized blockchain for the network for automobile ownership.**
<div align="center">
    <img src='image.png' />
    <br />
    <br />
</div>
</br>
There have been lots of cases of robbery, fraud, fake, etc of the vehicles in the automobile industry. Many a time, the stolen vehicle is illegally found in someone’s house with illegal ownership. The core motivation is to reduce the appearance of 3rd party agents for safe and secure transactions.</br>
The implementation of blockchain makes it easy to check a vehicle’s real history. Once data is entered into a blockchain, it becomes immutable, which means it can’t be changed. This eliminates data tampering and manipulation and dramatically reduces the risk of fraud. Since access to data is tracked, attempts to change data can be traced to the individual trying to make the changes. All of these features create a chain of trust that ensures that vehicle data remains accurate.</br>
Also, the transfer of vehicle ownership has always been a long, tedious process. It involves filling out multiple paper documents, approval from numerous people, and going through many processes. This not only takes a long time, but also opens up registration to human error, or worse, fraud or manipulation of data. With so many steps in the process, it also costs a lot. Blockchain makes all of this quicker, easier, and safer.</br>
Blockchain technology is all digital, which means there are no more cumbersome forms to fill out or paper records to search for. All the information is available and easily accessible. Smart contracts allow this information to be authenticated by the relevant people. The data is always available, making ownership transfer on future vehicle purchases even easier.</br>
The outline here is the demonstration of my idea and the curiosity in blockchain technology. It is a theoretical blockchain, implemented in Python, which is used as the tracking records of vehicle ownership.

---

# Details

In the industry, automobile companies have a particular vehicle identification number, which is a unique code. The government issues this serial code for the proper use and to trace the manufacture and purchase history of the particular vehicle. It is based on the concept that all the digital events or each transaction that have been executed are encoded in the public ledger, which is verified by consensus of a majority of the participants in the system. The decentralized peer ­to­ peer network/nodes of every single transaction ever made. </br>
 A few variables for the above theoretical transaction system :
 
 - Owner - Automobile Organization with a vehicle for sale: e.g., Hyundai Motor India Limited.
 - Receiver - Person buying the vehicle: e.g., **Maria Pedraza**
 - Amount - Fiscal value paid by **Maria Pedraza** for acquiring the vehicle from the automobile company.
 - Vec_ID - Serial code of vehicle being sold.
 
 
It is quite understandable that when Maria walks up to Hyundai to buy herself a new car, she initiates a transaction. This transaction records all these details and stores in the ledger. Now, when Maria decides to sell her vehicle, she becomes the owner, and Jamie, who's buying her car, becomes the receiver. Another, transaction is added to the chain. In these two transactions, we observe that we can preserve information regarding the automobile serial code while still tracking the movement of the vehicle from one hand to another.<br/>
This ledger nature of a blockchain also allows for Maia, Jamie, and Vivek to be updated about the movement of the particular automobile at the same time. If necessary, Maria can trace the records of the movement of a vehicle from initially to Vivek.

---

## Pre-requsites : 

A common understanding of blockchain and python basics is quite sufficient  to make to implement this project. I would recommend to go through some underlying priciples like Proof of Work, Hashing Algorithms, Data distribution for the deep learning of blockchain technology.<br/>
Some resources:

- https://bitsonblocks.net/2015/09/09/a-gentle-introduction-to-blockchain-technology/
- https://blockchain.berkeley.edu/courses/spring-2017-fundamentals-decal/
- https://www.youtube.com/watch?v=kP6EezXJKNM
- https://www.youtube.com/watch?v=UqQMSVfugFA&list=PLsyeobzWxl7oY6tZmnZ5S7yTDxyu4zDW-&index=1

---

## Packages Used:
- Flask app
- Requests <br/>
And use of Curl/Postman for making http request.
