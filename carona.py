import os
from sys import path
from time import sleep
from tkinter import *

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


# TODO: selenium.common.exceptions.NoSuchElementException
def fb_group_post(cidade):
    # Your Facebook account user and password
    usr = email_entry.get()
    pwd = senha_entry.get()
    links_grupos = []
    cidade_origem = ''

    if cidade == 'Muriaé':
        cidade_origem = 'Ouro Preto'
        links_grupos = ["https://www.facebook.com/groups/1973005072714372/", ]
    elif cidade == 'Ouro Preto':
        cidade_origem = 'Muriaé'
        links_grupos = ["https://www.facebook.com/groups/1973005072714372/", ]

    data_str = data.get()
    horario_str = horario.get()

    mensagem = "🔴 Procuro carona {0} >> {1} \n {2}, {3}" \
        .format(cidade_origem, cidade, data_str, horario_str)
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
    driver.implicitly_wait(15)  # seconds

    # Login to Facebook
    driver.get("http://www.facebook.com")
    elem = driver.find_element_by_id("email")
    elem.send_keys(usr)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    sleep(15)

    for group in links_grupos:

        # Go to the Facebook Group
        driver.get(group)

        # Click the post box
        sleep(10)
        post_box = driver.find_element_by_xpath("//*[@name='xhpc_message_text']")

        # Enter the text we want to post to Facebook
        post_box.send_keys(mensagem)
        sleep(10)

        # Get the 'Post' button and click on it
        try:
            # driver.get_screenshot_as_file("capture.png")
            post_button = driver.find_element_by_xpath(
                "//*[@data-testid='react-composer-post-button']")
            post_button.click()
            sleep(5)
        except:
            ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .send_keys(Keys.RETURN) \
                .key_up(Keys.CONTROL) \
                .perform()
        sleep(5)

    driver.close()
    return


def carona_handler():
    if destino_var.get() == 'Ouro Preto':
        print('Ouro Preto')
        desabilitar_elementos()
        fb_group_post(destino_var.get())
        habilitar_elementos()

    elif destino_var.get() == 'Muriaé':
        print('Muriaé')
        desabilitar_elementos()
        fb_group_post(destino_var.get())
        habilitar_elementos()
    else:
        print('Escolha uma opção.')


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
    login_form = Frame(master, relief="sunken", borderwidth="1")
    email_label = Label(login_form, text="E-mail do Facebook:")
    email_entry = Entry(login_form, width='31')
    senha_label = Label(login_form, text="Senha do Facebook:")
    senha_entry = Entry(login_form, show="*", width='31')
    login_form.pack()
    email_label.pack(anchor='w', padx='5')
    email_entry.pack(padx='5')
    senha_label.pack(anchor='w', padx='5')
    senha_entry.pack(padx='5')

    config_frame = Frame(master)
    destino_label = Label(config_frame, text='Destino:')
    destino_var = StringVar()
    destino_var.set('Carona para onde?')
    destino = OptionMenu(config_frame, destino_var, 'Ouro Preto', 'Muriaé')
    data = Entry(config_frame)
    data_label = Label(config_frame, text="Data:")
    horario = Entry(config_frame)
    horario_label = Label(config_frame, text='Horário:')
    config_frame.pack(fill='x')
    destino_label.pack(anchor='w', padx='5')
    destino.pack(fill='x', padx='5')
    data_label.pack(anchor='w', padx='5')
    data.pack(fill='x', padx='5')
    horario_label.pack(anchor='w', padx='5')
    horario.pack(fill='x', padx='5')

    procurar_botao = Button(config_frame, text='Procurar Carona!', command=carona_handler)
    procurar_botao.pack(anchor='e', padx='5', pady='5')

    mainloop()
