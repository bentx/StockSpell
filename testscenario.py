import secretIngredient
import dataUtility

response = dataUtility.getSwingStock().json()
data=[]
for stockdetail in response["data"]["results"]:
    data.append(stockdetail["stock"]["info"]["name"])
print(data)