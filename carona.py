import os
from sys import path
from time import sleep
from tkinter import *
from tkinter import messagebox

from selenium import common
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


# noinspection PyBroadException
def postar_no_facebook(email, senha, grupos, mensagem):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("dom.webnotifications.enabled", False)

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(firefox_options=options,
                               executable_path=os.path.join(path[0], 'geckodriver.exe'))
    driver.implicitly_wait(15)

    driver.get("http://www.facebook.com")
    elem = driver.find_element_by_id("email")
    elem.send_keys(email)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(senha)
    elem.send_keys(Keys.RETURN)
    sleep(15)

    for group in grupos:
        driver.get(group)

        sleep(10)
        try:
            post_box = driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
        except common.exceptions.NoSuchElementException:
            messagebox.showerror('Algo deu errado!',
                                 "Não foi possível logar no Facebook, tente novamente.")
            driver.close()
            return

        post_box.send_keys(mensagem)
        sleep(10)

        try:
            post_button = driver.find_element_by_xpath(
                "//*[@data-testid='react-composer-post-button']")
            post_button.click()
            sleep(5)
        except Exception:
            ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .send_keys(Keys.RETURN) \
                .key_up(Keys.CONTROL) \
                .perform()
        sleep(5)

    driver.close()
    messagebox.showinfo('Sucesso!', 'Todas as caronas foram postadas.')
    return


def carona_handler():
    # Muriaé >> Ouro Preto
    if origem_var.get() == 'Muriaé' and destino_var.get() == 'Ouro Preto':
        print('Muriaé >> Ouro Preto')
        grupos = ['https://www.facebook.com/groups/197987093613087/',
                  'https://www.facebook.com/groups/314296848663622/',
                  'https://www.facebook.com/groups/1487504921462576/',
                  'https://www.facebook.com/groups/1671840656410743/']

    # Ouro Preto >> Muriaé
    elif origem_var.get() == 'Ouro Preto' and destino_var.get() == 'Muriaé':
        print('Ouro Preto >> Muriaé')
        grupos = ['https://www.facebook.com/groups/197987093613087/',
                  'https://www.facebook.com/groups/314296848663622/',
                  'https://www.facebook.com/groups/1487504921462576/',
                  'https://www.facebook.com/groups/1671840656410743/']

    # Ouro Preto >> Viçosa
    elif origem_var.get() == 'Ouro Preto' and destino_var.get() == 'Viçosa':
        print('Ouro Preto >> Viçosa')
        grupos = ['https://www.facebook.com/groups/197987093613087/',
                  'https://www.facebook.com/groups/148666088555002/',
                  'https://www.facebook.com/groups/178889795534679/',
                  'https://www.facebook.com/groups/233530423442784/']

    # Viçosa >> Ouro Preto
    elif origem_var.get() == 'Viçosa' and destino_var.get() == 'Ouro Preto':
        print('Viçosa >> Ouro Preto')
        grupos = ['https://www.facebook.com/groups/197987093613087/',
                  'https://www.facebook.com/groups/148666088555002/',
                  'https://www.facebook.com/groups/178889795534679/',
                  'https://www.facebook.com/groups/233530423442784/']

    # Viçosa >> Muriaé
    elif origem_var.get() == 'Viçosa' and destino_var.get() == 'Muriaé':
        print('Viçosa >> Muriaé')
        grupos = ['https://www.facebook.com/groups/197987093613087/',
                  'https://www.facebook.com/groups/750505538437249',
                  'https://www.facebook.com/groups/289535414451046/']

    # Muriaé >> Viçosa
    elif origem_var.get() == 'Muriaé' and destino_var.get() == 'Viçosa':
        print('Muriaé >> Viçosa')
        grupos = ['https://www.facebook.com/groups/1973005072714372/', ]
    else:
        print('Escolha uma opção.')
        return

    email_str = email_entry.get()
    senha_str = senha_entry.get()

    origem_str = origem_var.get()
    destino_str = destino_var.get()
    data_str = data.get()
    horario_str = horario.get()
    mensagem = "🔴 Procuro carona {0} >> {1} \n {2}, {3}." \
        .format(origem_str, destino_str, data_str.capitalize(), horario_str)

    desabilitar_elementos()
    postar_no_facebook(email_str, senha_str, grupos, mensagem)
    habilitar_elementos()
    return


def desabilitar_elementos():
    for elemento in login_form.winfo_children():
        elemento.configure(state='disabled')
    for elemento in config_frame.winfo_children():
        elemento.configure(state='disabled')
    master.update()
    master.update_idletasks()
    return


def habilitar_elementos():
    for elemento in login_form.winfo_children():
        elemento.configure(state='normal')
    for elemento in config_frame.winfo_children():
        elemento.configure(state='normal')
    master.update()
    master.update_idletasks()
    return


if __name__ == '__main__':
    master = Tk()
    master.title('Caronator v1')

    # Elementos do formulário de login
    login_form = Frame(master, relief="sunken", borderwidth="1")
    email_label = Label(login_form, text="E-mail do Facebook:")
    email_entry = Entry(login_form, width='31')
    senha_label = Label(login_form, text="Senha do Facebook:")
    senha_entry = Entry(login_form, show="*", width='31')

    # Adciona os elementos do formulário de login à GUI
    login_form.pack()
    email_label.grid(sticky='w', padx='5')
    email_entry.grid(padx='5')
    senha_label.grid(sticky='w', padx='5')
    senha_entry.grid(padx='5', pady='5')

    # Elementos do formulário de carona
    config_frame = Frame(master)
    origem_label = Label(config_frame, text='Cidade de Origem:')
    destino_label = Label(config_frame, text='Cidade de Destino:')
    origem_var = StringVar()
    origem_var.set('Origem')
    destino_var = StringVar()
    origem = OptionMenu(config_frame, origem_var, 'Ouro Preto', 'Muriaé', 'Viçosa')
    origem.config(width=str(len('Ouro Preto')))
    destino_var.set('Destino')
    destino = OptionMenu(config_frame, destino_var, 'Ouro Preto', 'Muriaé', 'Viçosa')
    destino.config(width=str(len('Ouro Preto')))
    data = Entry(config_frame)
    data_label = Label(config_frame, text="Data:")
    horario = Entry(config_frame)
    horario_label = Label(config_frame, text='Horário:')

    # Adciona os elementos do formulário de carona à GUI
    config_frame.pack(fill='x')
    origem_label.grid(sticky='w', padx='5', column='0', row='0')
    destino_label.grid(sticky='w', padx='5', column='1', row='0')
    origem.grid(sticky='w', padx='5', column='0', row='1')
    destino.grid(sticky='w', padx='5', column='1', row='1')
    data_label.grid(sticky='w', padx='5', row='2')
    data.grid(sticky='ew', padx='5', row='3', columnspan='2')
    horario_label.grid(sticky='w', padx='5', row='4')
    horario.grid(sticky='ew', padx='5', row='5', columnspan='2')

    # Cria o botão e o coloca na GUI
    procurar_botao = Button(config_frame, text='Procurar Carona!', command=carona_handler)
    procurar_botao.grid(sticky='e', padx='5', pady='5', column='1', row='6')

    mainloop()
