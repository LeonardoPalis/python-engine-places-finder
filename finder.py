import requests
import json
from time import sleep
import sys
import csv
import re
#################################################################################
# Script usado para buscar locais em uma cidade especifica atraves de  busca por#
# keywords,ids  ou coordenadas e salva resultados no banco                      #
#                                                                               #
#################################################################################
aux = {}
pos = 0
lista = []
final_array = {}
API_KEY = "AIzaSyBNUqr5Uy-tNzI_wndhPw35r9n1WnVco9A" 


#=========================================================================#
# Metodo para pegar coordenadas de um local ou cidade por id              #
#=========================================================================# 
def getCoordenadasId(id_local, type_place):

	url_getLocal =  "https://maps.googleapis.com/maps/api/place/details/json?placeid="+str(id_local)+"&key="+API_KEY
	response_local = requests.get(url_getLocal)
	content = response_local.content
	parse_local = json.loads(content)
	resposta = parse_local['status']
	if(resposta == "OK"):
		name =  parse_local['result']['name']
		end =   parse_local['result']['vicinity']
		types = parse_local['result']['types']
		coo =   parse_local['result']['geometry']['location']
		try:
			rate =  parse_local['result']['rating']
		except Exception:
			rate = 0
    		pass

	else:
	    sys.exit("Erro ao processar requisicao.Metodo: getCoordenadasId(id_local). A API Place Details disse : " + resposta)
	
	#print "============================================================================================="
	#print "Place found:"	 
	#print "Name: " + name
	
	try:
		local_aux =  end.split('-')[1]
		try:
			neightborhood_aux =  local_aux.split(',')[0]
			print(neightborhood_aux)
		except Exception:
			pass

	except Exception:
		neightborhood_aux =  end.split('-')[0]
		#print "Location: " + neightborhood_aux
		pass
	result = {'name':name,'neightborhood':end,'typle_place':type_place,'rate':rate, 'neightborhood':neightborhood_aux}
	#print "Rate: " + str(rate)
	#print "Types: " + str(types)
	#print "Lat/Long: " + str(coo)
	#print "============================================================================================="
	#aux.extend(result)
	#aux[pos] = result
	
	lista.append(result)

	return result
	
d = { 'database.html': aux
}
def getPlaces_type(type_p,query,type_local):
	print "Finding place ..."
	url_lugares  = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+type_p+query+"&type="+type_local+"&libraries=places&key="+API_KEY
	request_lugares = requests.get(url_lugares)
	parse_l = json.loads(request_lugares.content)
	#print parse_l
	response = parse_l['status']
	if(response == "OK"):
	    print "Find details ..."
	    #inicializa dicionario que ira conter os lugares 
	    locais = {}
	    x = 0  
	    #loop para percorrer resultados da busca
	    for i in  parse_l['results']:
		#indice para dicionario
		x = x + 1
		#pega lat,lng e id do local 
		id_lugar  =  i['place_id']
		#coloca o dicionario do local no dicionario de resultados 
		locais[x] = getCoordenadasId(id_lugar,type_p)
		#aux.extend(locais[x])
		
		#print locais[x]
		#print x
	else:
	    sys.exit("ERROR API MAPS: " + response)
	return locais

type_places_style = {'rock', 'samba', 'pagode', 'metal', 'pop', 'sertaneja', 'italiana', 'mexicana', 'japonesa', 'brasileira', 'tailandesa', 'chinesa', 'indiana', 'arabe' }
type_places_style_aux = {'rock'}

x = 0
l =  getPlaces_type("italiana", "Belo Horizonte", "restaurant")
print l
#

# for i in type_places_style:
# 	print("TYPE: " + i)
# 	l =  getPlaces_type(i, "Belo Horizonte", "restaurant")
# 	#print(l)

# d = { 'database.html': 
#       {'dail': 1,
#        'focus': 1,
#        'actions': 1,
#        'trade': 2,
#        'protest': 1,
#        'identify': 1 }
# }


# for original_filename in d.keys():
#     m = re.search('^(.*)\.html$',original_filename)
#     if not m:
#         print "Ignoring the file:", original_filename
#         continue
#     output_filename = m.group(1)+'.arff'
#     with open(output_filename,"w") as fp:
#         fp.write('''@RELATION places

# @ATTRIBUTE type_place { rock, samba, pagode, metal, pop, sertaneja, italiana, mexicana, japonesa, brasileira, tailandesa, chinesa, indiana, arabe}
# @ATTRIBUTE rate numeric
# @ATTRIBUTE neightborhood string

# ''')
#         fp.write("@DATA\n")
#     	for j in lista:
# 			fp.write(j["name"].encode("unicode_escape") + "," + str(j["rate"]) + "," + j["typle_place"] + "," + j["neightborhood"].encode("unicode_escape") +"\n")