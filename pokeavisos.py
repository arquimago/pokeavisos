#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, Job
from datetime import datetime

#arqTokens = open('pokeavisos.token','r')
#token = arqTokens.read()
#arqTokens.close()
token = 


updater = Updater(token=token)
dispatcher = updater.dispatcher

j = updater.job_queue
headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Accept-Encoding':'gzip, deflate','Accept-Language':'pt-BR,pt;q=0.9,en-XA;q=0.8,en;q=0.7,en-US;q=0.6','Cache-Control':'no-cache','Connection':'keep-alive','Content-Length':'1763','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Cookie':'BISCOITO','Host':'host','Origin':'http://abc.com','Pragma':'no-cache','Referer':'http://abc.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 X-Requested-With:XMLHttpRequest'}
payload = {'timestamp':'0','pokemon':'true','lastpokemon':'true','pokestops':'false','lastpokestops':'false','luredonly':'false','gyms':'false','lastgyms':'false','exEligible':'false','scanned':'false','lastslocs':'false','spawnpoints':'false','lastspawns':'false','minIV':'90','prevMinIV':'0','minLevel':'25','prevMinLevel':'0','bigKarp':'false','tinyRat':'false','swLat':'-11.074225690906626','swLng':'-37.27662977772229','neLat':'-10.820408408519448','neLng':'-37.10908827381604','oSwLat':'-11.074225690906626','oSwLng':'-37.27662977772229','oNeLat':'-10.820408408519448','oNeLng':'-37.10908827381604','reids':'','eids':'','exMinIV':'131,143,147,148,149,242,247,248,289,306,349,350,371,372,373,374,375,376','token':'Kl6jiM2hz7WR0157CAo3+0TwKPeOqRGxjVGoAfL+gSQ='}
request_url = 'URL DE REQUEST AQUI'
headers["Origin"]= 'URL DE ORIGEM AQUI'
headers["Referer"] = 'URL REFERER AQUI'
headers["Host"] = 'URL DO HOST AQUI"
headers["Cookie"] = 'Cookie Aqui"
sessao = requests.Session()
sessao.headers.update(headers)

def get_pokes():
	global sessao
	global payload
	global request_url
	r = sessao.post(request_url, data = payload).json()
	payload["timestamp"]=int(time.time())
	return r

def start(bot, update):	  
	bot.sendMessage(chat_id=update.message.chat_id, text="Este bot avisa de pokemons!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def git(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="O código deste bot se encontra em http://github.com/arquimago/pokeavisos")

git_handler = CommandHandler('git', git)
dispatcher.add_handler(git_handler)

def confere_pokemons(bot, job):
	lista = get_pokes()
	tamanho = len(lista["pokemons"]) 
	if tamanho == 0:
		print("0 pokemnons encontrados\n"  + str(datetime.fromtimestamp(time.time())) + '\n')
		return
	
	for i in range(0,tamanho):
		mensagem = "Encontrado " + lista["pokemons"][i]["pokemon_name"] +'\n'
		timestamp = lista["pokemons"][i]["disappear_time"]/1000
		hora = "desaparece " + str(datetime.fromtimestamp(timestamp)) + '\n'
		mensagem += hora
		ataque = lista["pokemons"][i]["individual_attack"]
		defesa = lista["pokemons"][i]["individual_defense"]
		vida = lista["pokemons"][i]["individual_stamina"]
		if ataque != 'null' and defesa != 'null' and vida != 'null':
			IV = round(((ataque+defesa+vida)/45)*100, 1)
			IVtexto = str(ataque) + "/" + str(defesa) + "/" + str(vida) + "\n IV: " + str(IV) + '\n'
		else:
			IVtexto = "não definido"
		mensagem += IVtexto
		nivel = lista["pokemons"][i]["level"]
		CP = lista["pokemons"][i]["cp"]
		lvltexto = "lvl:" + str(nivel) + " CP: " + str(CP) + '\n'
		mensagem += lvltexto
		raridade = lista["pokemons"][i]["pokemon_rarity"]
		mensagem += raridade
		latitude = float(lista["pokemons"][i]["latitude"])
		longitude = float(lista["pokemons"][i]["longitude"])
		chat = "@pokeavisosaju"
		print("pokemon enviado\n" + str(time.time()) + '\n' )
		bot.sendMessage(chat,text=mensagem)
		bot.sendLocation(chat, latitude , longitude)
		
		
j.run_repeating(confere_pokemons, 10.0, first=0)

updater.start_polling()
