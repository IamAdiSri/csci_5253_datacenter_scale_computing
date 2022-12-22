
|          **Method** | **Local**             | **Same Zone**         | **Different Region**  |
|--------------------:|-----------------------|-----------------------|-----------------------|
|        **REST add** | 2.229045389000021 ms  | 2.3875692500000696 ms | 285.861591799 ms      |
|        **gRPC add** | 0.4743962330003342 ms | 0.495292628000243 ms  | 142.86321718999943 ms |
|     **REST rawimg** | 3.08143739299976 ms   | 5.726508399999602 ms  | 1175.2080615999996 ms |
|     **gRPC rawimg** | 3.129563685999983 ms  | 3.952889142999993 ms  | 193.1468532300005 ms  |
| **REST dotproduct** | 2.678845987999921 ms  | 2.997879759999705 ms  | 288.0737209999995 ms  |
| **gRPC dotproduct** | 0.6549964989999353 ms | 0.6178274399999282 ms | 143.23143580000078 ms |
|    **REST jsonimg** | 75.1684344690002 ms   | 73.46576186699986 ms  | 1356.8663629000002 ms |
|    **gRPC jsonimg** | 27.29696983599979 ms  | 28.544676582999728 ms | 232.141798130001 ms   |
|            **Ping** | 0.035 ms              | 0.354 ms              | 141.635 ms            |

>> You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

>> You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

The most noticeable difference is the increase in time as the distance between the server and the client increases. As is to be expected, the time taken for all operations is least when the server and client reside locally on the same machine, followed by when they are located in the same zone (i.e. `us-west`), and greatest when the server and client are located far apart (i.e. `us-west` and `eu-west`). This is caused due to the fact that messages between the client and the server travel physically between the two and thus have to cover the actual distance between them.

The differences between the results of the two protocols, REST and gRPC, can be boiled down to three characteristics - the first being networking overhead, the second being processing overhead, and the third being payload size. First, as stated above, every time we pass a message through the REST protocol a new TCP connection must be created and must be closed after the messages have gone through, which incurs a bit of time penalty at each query. gRPC on the other hand, creates a single TCP connection between the client and the server and maintains it for the entire duration of the client operations. Thus the penalty is incurred only once over the entire process. 

Second, messages passed through the REST protocol generally travel as JSON, and which encodes information as key-value pairs, where the data is often in the form of strings. Thus, both the client and the server have to perform string processing and type inferencing to encode and decode the JSON payload before it can be used, which adds processing overhead. In comparison, gRPC is strongly typed and transfers data in efficient binary encoding. This saves both the client and the server some work by avoiding type inferencing and the binary data also allows for quicker processing.

Finally, while JSON is more flexible, it is also more inefficient at encoding data than gRPC. Since the keys and values may be encoded as text, the size of the JSON payload can get quite large as the complexity of the data to be transferred increases. In comparison, since both the client and the server have prior knowledge about the messages that will be sent/received over the gRPC protocol, the encoding of the payload can be made simpler and more compact, which reduces the size of the payload. Smaller payloads are faster to transfer, thus the gRPC protocol performs better.
