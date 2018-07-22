import os
from sys import path
from time import sleep
from tkinter import *
from tkinter import messagebox

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def postar_no_whatsapp(grupos, mensagem):
    global sucesso_wp
    print('Postando no Whatsapp')
    options = Options()
    # options.add_argument("--headless")

    driver = webdriver.Firefox(firefox_options=options,
                               executable_path=os.path.join(path[0], 'geckodriver.exe'))
    driver.get("https://web.whatsapp.com/")

    wait = WebDriverWait(driver, 900)

    for grupo in grupos:
        x_arg = '//span[contains(@title, ' + '"' + grupo + '"' + ')]'
        janela_de_conversa = wait.until(ec.presence_of_element_located((
            By.XPATH, x_arg)))

        janela_de_conversa.click()
        caixa_de_texto_caminho = \
            '//div[@class="_2S1VP copyable-text selectable-text"][@dir="ltr"][@data-tab="1"]'
        caixa_de_texto = wait.until(ec.presence_of_element_located((
            By.XPATH, caixa_de_texto_caminho)))

        for parte in mensagem.split('\n'):
            caixa_de_texto.send_keys(parte)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(
                Keys.SHIFT).key_up(Keys.ENTER).perform()
        caixa_de_texto.send_keys(Keys.ENTER)
        sleep(20)

    sucesso_wp = True
    driver.close()


def postar_no_facebook(email, senha, grupos, mensagem):
    # Criar instância do navegador
    driver = webdriver.Firefox()

    # Minimiza a janela do navegador.
    driver.minimize_window()

    # Acessa a página de login do Facebook
    driver.get("https://mbasic.facebook.com")

    # Encontrar elemento do campo de e-mail pelo atributo
    email_field = driver.find_element_by_name("email")

    # Digita o e-mail no campo de e-mail pelo atributo
    email_field.send_keys(email)

    # Encontrar elemento do campo de senha pelo atributo
    senha_field = driver.find_element_by_name("pass")

    # Digita a senha no campo de senha pelo atributo
    senha_field.send_keys(senha)

    # Simular que o enter seja precisonado
    driver.find_element_by_name("pass").send_keys(Keys.ENTER)

    # Espera 5 segundos
    sleep(5)

    # Verifica se fez login no Facebook
    try:
        driver.find_element(By.XPATH, "//input[@value='OK']").click()
    except NoSuchElementException:
        messagebox.showerror('Algo deu errado!',
                             "Não foi possível logar no Facebook, tente novamente.")
        driver.close()
        return

    # Espera 5 segundos
    sleep(5)

    for grupo in grupos:
        # Acessa o grupo do Facebook
        driver.get(grupo)

        # Espera a pagina ser carregada se a internet estiver lenta
        driver.set_page_load_timeout(60 * 50)

        # Pega o nome do Grupo do Facebook que está acessando.
        nome_grupo = driver.title

        # Informa qual grupo foi acessado
        print('\n')
        print('Acessando grupo: "{}"'.format(nome_grupo))
        try:
            # Encontrar elemento do campo de postagem pelo atributo
            caixa_mensagem = driver.find_element_by_name("xc_message")

            # Digita a mensagem no campo de postagem pelo atributo
            caixa_mensagem.send_keys(mensagem)

            # Informa que está sendo postado a mensagem
            print('Adicionando mensagem à caixa')

            # Espera a pagina ser carregada se a internet estiver lenta
            driver.set_page_load_timeout(60 * 50)

            try:
                # Encontrar elemento do campo de publicar pelo atributo
                driver.find_element_by_name("view_post").click()
            except NoSuchElementException:
                ActionChains(driver) \
                    .key_down(Keys.CONTROL) \
                    .send_keys(Keys.RETURN) \
                    .key_up(Keys.CONTROL) \
                    .perform()

            # Informa que foi finalizado no grupo que está sendo postado
            print('Postagem realizada com sucesso.')

        except NoSuchElementException as e:
            print('Não foi possível postar no grupo.')
            print(e)

        # Espera 5 segundos
        sleep(5)

    # Fechar navegador
    driver.quit()


def carona_handler():
    global sucesso_fb
    global sucesso_wp
    email_str = email_entry.get()
    senha_str = senha_entry.get()

    origem_str = origem_var.get()
    destino_str = destino_var.get()
    data_str = data.get()
    horario_str = horario.get()
    mensagem = "🔴 Procuro carona {0} >> {1} \n {2}, {3}." \
        .format(origem_str, destino_str, data_str.capitalize(), horario_str)

    grupos_wp = []
    grupos_fb = []

    if not postagem_fb_var.get() and not postagem_wp_var.get():
        messagebox.showerror('Algo deu errado',
                             'Você precisa selecionar ao menos um lugar para procurar sua '
                             'carona.')
        return

    if postagem_fb_var.get() and not email_str or not senha_str:
        messagebox.showerror('Algo deu errado',
                             'Você deixou alguns campos vazios, preencha-os.')
        return

    if origem_str == 'Origem' or destino_str == 'Destino' or not data_str \
            or not horario_str or not mensagem:
        messagebox.showerror('Algo deu errado',
                             'Você deixou alguns campos vazios, preencha-os.')
        return

    messagebox.showinfo('Aguarde.', 'O Caronator agora irá tentar postar os pedidos de carona '
                                    'com as configurações que você especificou, '
                                    'pressione Ok e aguarde.')

    # Muriaé >> Ouro Preto
    if origem_var.get() == 'Muriaé' and destino_var.get() == 'Ouro Preto':
        print('Muriaé >> Ouro Preto')
        grupos_fb = ['https://mbasic.facebook.com/groups/197987093613087/',
                     'https://mbasic.facebook.com/groups/314296848663622/',
                     'https://mbasic.facebook.com/groups/1487504921462576/',
                     'https://mbasic.facebook.com/groups/1671840656410743/']
        grupos_wp = ['Carona: 🚗BH<>🚘<>Muriaé🚕', ]

    # Ouro Preto >> Muriaé
    elif origem_var.get() == 'Ouro Preto' and destino_var.get() == 'Muriaé':
        print('Ouro Preto >> Muriaé')
        grupos_fb = ['https://mbasic.facebook.com/groups/197987093613087/',
                     'https://mbasic.facebook.com/groups/314296848663622/',
                     'https://mbasic.facebook.com/groups/1487504921462576/',
                     'https://mbasic.facebook.com/groups/1671840656410743/']
        grupos_wp = ['Carona: 🚗BH<>🚘<>Muriaé🚕', ]

    # Ouro Preto >> Viçosa
    elif origem_var.get() == 'Ouro Preto' and destino_var.get() == 'Viçosa':
        print('Ouro Preto >> Viçosa')
        grupos_fb = ['https://mbasic.facebook.com/groups/197987093613087/',
                     'https://mbasic.facebook.com/groups/148666088555002/',
                     'https://mbasic.facebook.com/groups/178889795534679/',
                     'https://mbasic.facebook.com/groups/233530423442784/']
        grupos_wp = ['Viçosa 《=》 BHte 🚙🤝💰', 'Carona Viçosa-OP-Viçosa🚕']

    # Viçosa >> Ouro Preto
    elif origem_var.get() == 'Viçosa' and destino_var.get() == 'Ouro Preto':
        print('Viçosa >> Ouro Preto')
        grupos_fb = ['https://mbasic.facebook.com/groups/197987093613087/',
                     'https://mbasic.facebook.com/groups/148666088555002/',
                     'https://mbasic.facebook.com/groups/178889795534679/',
                     'https://mbasic.facebook.com/groups/233530423442784/']
        grupos_wp = ['Viçosa 《=》 BHte 🚙🤝💰', 'Carona Viçosa-OP-Viçosa🚕']

    # Viçosa >> Muriaé
    elif origem_var.get() == 'Viçosa' and destino_var.get() == 'Muriaé':
        print('Viçosa >> Muriaé')
        grupos_fb = ['https://mbasic.facebook.com/groups/197987093613087/',
                     'https://mbasic.facebook.com/groups/750505538437249',
                     'https://mbasic.facebook.com/groups/289535414451046/']
        grupos_wp = []

    # Muriaé >> Viçosa
    elif origem_var.get() == 'Muriaé' and destino_var.get() == 'Viçosa':
        print('Muriaé >> Viçosa')
        grupos_fb = ['https://mbasic.facebook.com/groups/197987093613087/',
                     'https://mbasic.facebook.com/groups/750505538437249',
                     'https://mbasic.facebook.com/groups/289535414451046/']
        grupos_wp = []

    # Teste >> Teste
    elif origem_var.get() == 'Teste' and destino_var.get() == 'Teste':
        print('Teste')
        grupos_fb = ['https://mbasic.facebook.com/groups/1973005072714372/']
        grupos_wp = []

    desabilitar_elementos()

    if grupos_fb and postagem_fb_var.get():
        postar_no_facebook(email_str, senha_str, grupos_fb, mensagem)
    if grupos_wp and postagem_wp_var.get():
        postar_no_whatsapp(grupos_wp, mensagem)

    habilitar_elementos()

    if postagem_fb_var.get() and sucesso_fb and sucesso_wp and postagem_wp_var.get():
        messagebox.showinfo('Sucesso!', 'As postagens foram feitas no Facebook e '
                                        'Whatsapp com sucesso.')
    elif postagem_fb_var.get() and sucesso_fb \
            and not sucesso_wp or not postagem_wp_var.get():
        messagebox.showinfo('Sucesso!', 'A postagem foi feita no Facebook com sucesso.')
    elif not postagem_fb_var.get() or not sucesso_fb \
            and sucesso_wp and postagem_wp_var.get():
        messagebox.showinfo('Sucesso!', 'A postagem foi feita no Whatsapp com sucesso.')

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

    origem_e_destino = ['Ouro Preto', 'Muriaé', 'Viçosa', 'Teste']

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
    destino_var = StringVar()
    origem = OptionMenu(config_frame, origem_var, *origem_e_destino)
    origem.config(width=str(len('Ouro Preto')))
    destino = OptionMenu(config_frame, destino_var, *origem_e_destino)
    destino.config(width=str(len('Ouro Preto')))
    data = Entry(config_frame)
    data_label = Label(config_frame, text="Data:")
    horario = Entry(config_frame)
    horario_label = Label(config_frame, text='Horário:')
    check_label = Label(config_frame, text='Onde deseja procurar:')
    postagem_fb_var = IntVar()
    postagem_fb_check = Checkbutton(config_frame, text='Facebook', variable=postagem_fb_var)
    postagem_wp_var = IntVar()
    postagem_wp_check = Checkbutton(config_frame, text='Whatsapp', variable=postagem_wp_var)

    # Adciona os valores as variáveis do tkinter
    origem_var.set('Origem')
    destino_var.set('Destino')
    postagem_fb_check.select()
    postagem_wp_check.select()

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
    check_label.grid(sticky='w', padx='5', row='6')
    postagem_fb_check.grid(sticky='w', padx='5', row='7', column='0')
    postagem_wp_check.grid(sticky='w', padx='5', row='7', column='1')

    # Cria o botão e o coloca na GUI
    procurar_botao = Button(config_frame, text='Procurar Carona!', command=carona_handler)
    procurar_botao.grid(sticky='e', padx='5', pady='5', column='1', row='8')

    sucesso_fb = False
    sucesso_wp = False
    mainloop()
