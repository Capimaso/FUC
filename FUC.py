#feira of science

#imports
from colorama import Fore, Back
import gtts
from os import system, startfile
import psutil
import pygame
from random import randint
import speech_recognition as sr
from time import sleep
from webbrowser import open


#Variables global
chamado = None
frase = None
voice_record = False
teste = False
tts = False

piadas = ["Quer ouvir uma piada sobre potássio?", "Faça como um próton,", "Contei uma piada de química no auditório,", "O que os outros elementos falam do hidrogênio:", "O que falaram para o carbono quando ele foi preso?", "Você acha um elétron e leva ele pra casa. Qual é o nome dele?", "O que um cromossomo disse para o outro?"]
respostas = ["K K K K K", "e fique positivo.", "mas a plateia não esboçou reação.", "Que ele é um solitário!!!", "Que ele tem direito a quatro ligações!", "Eletrondoméstico.", "Cromossomos felizes!"]
# ===============functions===================

#------------menos importantes------------

#caso der erro volta pro menu
def erro():
    system('cls')
    texto("Comando não reconhecido")
    menu()

#loading
def loading(tempo, texto):
    carregando = True
    pontos = 0
    while carregando == True:
        system('cls')
        print(texto, end="")
        print("." * pontos)
        sleep(tempo)
        pontos += 1
        if pontos == 4:
            system('cls')
            break

#---------------muito importantes-------------------------  
#resposta ser em voice ou text
def resposta(voice, text):
    if voice_record == True:
        resposta = reconhecer_voz(voice)
    elif voice_record == False:
        resposta = input(text)
    return resposta

# fecha os possiveis navegadores abertos
def close_possible_browsers():
    # Lista de possíveis executáveis de navegadores
    browser_executables = [
        'chrome.exe',  # Google Chrome
        'firefox.exe',  # Mozilla Firefox
        'opera.exe',  # Opera
        'msedge.exe',  # Microsoft Edge
    ]
    for browser in browser_executables:
        try:
            browser_found = False
            # Itera sobre todos os processos em execução
            for proc in psutil.process_iter(['pid', 'name']):
                # Verifica se o processo corresponde ao nome do navegador especificado
                if proc.info['name'].lower() == browser:
                    # Fecha o processo
                    proc.terminate()
                    browser_found = True
                    print(f"Processo {browser} com PID {proc.info['pid']} foi encerrado.")
            if not browser_found:
                print(f"{browser} não está em execução.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"Erro ao tentar fechar o {browser}: {e}")

# pesquisa 
def pesquisar_no_google():
    # Solicita ao usuário que insira o termo de pesquisa
    pesquisa = resposta("Estou ouvindo, o que gostaria de pesquisar? \n > ", "O que gostaria de pesquisar? \n > ")

    # Codifica a pesquisa para o formato de URL
    url = "https://www.google.com/search?q=" + pesquisa.replace(' ', '+')

    # Abre a URL no navegador padrão
    open(url)

    response = resposta("Você gostaria de continuar pesquisando?", "Continuar pesquisando? \n > ")
    response.lower()
    if "não" in response:
        print("Ok")
        close_possible_browsers()
        system('cls')
    elif "parar" in response:
        print("Ok")
        close_possible_browsers()
        system('cls')

    elif "sim" in response: 
        pesquisar_no_google()
    elif "continuar" in response:
        pesquisar_no_google()  
    elif "pesquisando" in response:
        pesquisar_no_google()

#reconhecimento de voz
def reconhecer_voz(text):
    rec = sr.Recognizer()
    global teste
    #usar with pra abrir e quando acabar de usar ja fechar o mic
    #!!!!!!!!!!!!!!mudar o sr.Microphone(1) no dia pra achar o correto!!!!!!!!!!!!!!!!!
    #print(sr.Microphone().list_microphone_names())             <- pra ver lista de mics 
    with sr.Microphone(1) as mic:
        rec.adjust_for_ambient_noise(mic)
        print(text)
        if teste == True:
            try:
                #capta o audio do mic e bota dentro da variavel audio
                audio = rec.listen(mic, timeout=15)
                texto = rec.recognize_google(audio, language="pt-BR")
                print(texto.capitalize())
                sleep(1)
                teste = False
                return(texto)
            except sr.WaitTimeoutError:
                print("Nenhum som detectado.")
                teste = False
                return None
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio.")
                teste = False
                return(reconhecer_voz("Por favor, tente novamente."))
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento de voz: {e}")
                teste = False
            return None
        
        elif teste == False:
                    try:
                        #capta o audio do mic e bota dentro da variavel audio
                        audio = rec.listen(mic, timeout=300)
                        texto = rec.recognize_google(audio, language="pt-BR")
                        if chamado in texto:
                            texto = texto.replace(chamado, "")
                            print(texto)
                            sleep(1)
                            return(texto)
                        elif chamado not in texto:
                            return(reconhecer_voz(""))
                    except sr.WaitTimeoutError:
                        print("")
                        return(reconhecer_voz(" "))
                    except sr.UnknownValueError:
                        print("Não foi possível entender o áudio.")
                        return(reconhecer_voz("Por favor, tente novamente."))
                    except sr.RequestError as e:
                        print(f"Erro no serviço de reconhecimento de voz: {e}")
                    return(reconhecer_voz("Por favor, tente novamente."))
        else:
            acessibilidade()
        
#tts
def tts_speaker(text):
    global frase
    frase = gtts.gTTS(text, lang='pt-br') 
    frase = frase.save('frase.mp3')
    falar('frase.mp3')

#fecha o audio
def close_audio():
    # Parando o áudio e fechando o mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def falar(frase):
    # Inicializando o mixer do pygame
    pygame.mixer.init()
    # Carregando o arquivo de áudio
    pygame.mixer.music.load(frase)
    # Reproduzindo o arquivo de áudio
    pygame.mixer.music.play()
    # Aguardando até que o áudio termine
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    close_audio()

def texto(text):
    if tts == False:
        print(text)

    elif tts == True:
        print(text)
        tts_speaker(text)

#mensagem de boas vindas
def welcome():
    texto("Bem vindo ao Computador simples.")
    menu()

#menu inicial
def menu():
    print("Digite ajuda para ver os comandos disponiveis: ")
    response = resposta("Captando sua bela voz!", "> ")
    if response == None:
        erro()
    elif "acessibilidade" in response:
        system('cls')
        acessibilidade()

    elif "slide" in response:
        system('cls')
        slide()

    elif "pesquisa" in response:
        pesquisar_no_google()
        loading(.5, "Voltando ao menu")
        menu()

    elif "piada" in response:
       piada()
    elif "ajuda" in response:
        system('cls')
        comandos()
    elif "creditos" in response or "criadores" in response:
        texto("Os criadores desse programa foram Tiago e João")
        if tts == False:
            sleep(2)
        system('cls')
        menu()
    else:
        erro() 
        
# piada
def piada():
    number = randint(0, len(piadas) - 1)
    piada = piadas[number]
    resposta = respostas[number]
    texto(piada)
    if tts == False:
        sleep(3)
    stop = input("Aperte enter para ver a resposta:")
    texto(resposta)
    if tts == False:
        sleep(3)
    system('cls')
    menu()
    
# Menu de slide                 pronto!
def slide():
    texto("Recomendamos duas plataformas para fazer slides:")
    texto("Canva, uma forma simples e prática")
    sleep(2)
    texto("Powerpoint, mais dificil, porém resultados mais bonitos")
    sleep(2)
    texto("Qual você gostaria de utilizar? \n Canva ou Powerpoint?")
    sleep(2)
    response = resposta("Ouvindo sua bela voz! \n >", "> ")
    if "canva" in response.lower():
        open("https://www.canva.com")
        loading(.5, "Voltando ao menu")
        menu()

    elif "powerpoint" in response.lower():
        startfile("POWERPNT.exe")
        loading(.5, "Voltando ao menu")
        menu()
    
    elif response == None:
        erro()

    else:
        system('cls')
        texto("Comando não reconhecido, tente novamente.")
        slide()

# Menu de acessibilidade
def acessibilidade():
    global voice_record
    global teste
    global tts
    texto("As acessibilidades disponiveis atualmente são:")
    texto("Reconhecimento de voz - Usado para você falar os comandos ao invés de escrever")
    texto("Tts - Text-To-Speech, O computador irá falar os textos")
    response = resposta("Ouvindo sua bela voz!", "> ")
    #=====speech recognition=====
    if "voz" in response.lower():
            global chamado
            voice_record = not voice_record
            teste = True
            texto("Vamos testar seu microfone?")
            response = resposta("Estou te ouvindo! Pode falar!", "> ")
            if response != None:
                loading(.5, "Voltando ao menu")
                texto("Qual seria sua palavra de chamado?")
                chamado = str(input("O que: "))
                teste = False
                menu()
            if response == None:
                voice_record = False
                stop = input("Microfone não reconhecido. Aperte enter para voltar ao menu")
                loading(.5, "Voltando ao menu")
                menu()
    
    #=====tts=====
    elif "tts":
        tts = not tts
        system('cls')
        menu()

    else:
        erro()
        
#menu pra mostrar os comandos (facilita dps pra n ficar procurando)
def comandos():
    texto("Acessiblidade - Mostra as opções de acessibilidade disponiveis.")
    texto("Menu - Volta para o menu principal")
    texto("Pesquisa - Permite fazer uma pesquisa no google")
    texto("Piadas inteligentes - Conta uma piada inteligente")
    texto("Slide - Mostra as opções disponiveis para realizar slides.")
    texto("Créditos - Mostra os criadores do aplicativo.")

    #para pra ler e dps limpa 
    response = resposta("Fale qualquer coisa para prosseguir.", "Aperte enter para continuar!")
    system('cls')
    #volta pro menu
    menu()

# program
system('cls')
welcome()