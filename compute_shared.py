import sys

p = 0x00ae0f0301f2ce3a97f40a5bded472bf9a168463aa1557b9888f502163d36f8f275816d971f3a40d3783dbe012077819d1081e5df45e978e26a03f2bc33aacf999998ca4673e551604d956c4b7641b534f74b7e96ffe27cc7f586e01c988d23e928abfc66125f97e73c6159622a6fa36551f0d40e8033a7245922ec797f6ebefac316e81641943527826a62dd62c83383f2b74e3e88b6210986c6dd54a9df092188f926294c87150550c862c2c74fd6bb7536c63ff121c7c82f6bfa5c466df8a2498de95f2ee65b62e1af7f1e2a441b50526c7d763bdb2e2da497bf6dde1b0552a39b91ca90e4f335465bf9483143c034e771b6245adc505c87e128f2054ecbce3
g = 2

f = open("secret.txt", "r")
a = int(f.readlines()[0])
f.close()

g_b = int(sys.argv[1])

g_b_a = pow(g_b, a, p)

f_out = open("shared_secret.txt", "w")
f_out.write(str(g_b_a))
f_out.close()
print("Success")