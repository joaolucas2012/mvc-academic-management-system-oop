import tkinter as tk
from tkinter import messagebox
import os.path
import pickle

# Exceptions de tratamento
class PreenchaTudo(Exception):
    pass
class NomeRepetido(Exception):
    pass

class CodeRepetido(Exception):
    pass

class Nome_Code_Repetido(Exception):
    pass

class CargaInvalida(Exception):
    pass

class NomeIsNumero(Exception):
    pass

class NomeInvalido(Exception):
    pass

class CodeInvalido(Exception):
    pass

class Disciplina:
    # Construtor
    def __init__(self, codigo, nome, cargaHoraria):
        self.__codigo = codigo
        self.__nome = nome
        self.__cargaHoraria = cargaHoraria

    def getCodigo(self):
        return self.__codigo

    def getNome(self):
        return self.__nome
    
    def getCargaHoraria(self):
        return self.__cargaHoraria

class LimiteInsereDisciplinas(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('250x100')
        self.title('Inserir disciplina')
        self.controle = controle

        self.frameCode = tk.Frame(self)
        self.frameCode.pack()
        self.labelCode = tk.Label(self.frameCode, text = 'Código:            ')
        self.labelCode.pack(side = 'left')
        self.inputCode = tk.Entry(self.frameCode, width = 20)
        self.inputCode.pack(side = 'left')

        self.frameNome = tk.Frame(self)
        self.frameNome.pack()
        self.labelNome = tk.Label(self.frameNome, text = 'Nome:              ')
        self.labelNome.pack(side = 'left')
        self.inputNome = tk.Entry(self.frameNome, width = 20)
        self.inputNome.pack(side = 'left')

        self.frameCarga = tk.Frame(self)
        self.frameCarga.pack()
        self.labelCarga = tk.Label(self.frameCarga, text = 'Carga horária: ')
        self.labelCarga.pack(side = 'left')
        self.inputCarga = tk.Entry(self.frameCarga, width = 20)
        self.inputCarga.pack(side = 'left')

        self.frameButtons = tk.Frame(self)
        self.frameButtons.pack()
        
        self.buttonInsere = tk.Button(self.frameButtons, text = 'Inserir', font = ('Negrito', 9))
        self.buttonInsere.pack(side = 'left')
        self.buttonInsere.bind("<Button>", controle.insereHandler)

        self.buttonLimpar = tk.Button(self.frameButtons, text = 'Limpar', font = ('Negrito', 9))
        self.buttonLimpar.pack(side = 'left')
        self.buttonLimpar.bind("<Button>", controle.ClearHandler)

        self.buttonConcluido = tk.Button(self.frameButtons, text = 'Concluído', font = ('Negrito', 9))
        self.buttonConcluido.pack(side = 'left')
        self.buttonConcluido.bind("<Button>", controle.concluiHandler)

class LimiteMostraDisciplinas():
    def __init__(self, str):
        messagebox.showinfo('Disciplinas cadastradas', str)

class CtrlDisciplina():
    def __init__(self):
        if not os.path.isfile("disciplina.pickle"):
            self.listaDisciplinas = []
        else:
            with open("disciplina.pickle", "rb") as f:
                self.listaDisciplinas = pickle.load(f)
    
    def salvaDisciplinas(self):
        if len(self.listaDisciplinas) != 0:
            with open("disciplina.pickle", "wb") as f:
                pickle.dump(self.listaDisciplinas, f)

    def mensagem(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

    def getListaDisciplinas(self):
        return self.listaDisciplinas

    def getDisciplina(self, codDisc):
        discRet = None
        for disc in self.listaDisciplinas:
            if disc.getCodigo() == codDisc:
                discRet = disc
        return discRet

    def getListaCodDisciplinas(self):
        listaCod = []
        for disc in self.listaDisciplinas:
            listaCod.append(disc.getCodigo())
        return listaCod
    
    def isNumber(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False

    def insereDisciplina(self):
        self.limiteIns = LimiteInsereDisciplinas(self)

    def mostraDisciplinas(self):
        if len(self.listaDisciplinas) == 0:
            str = 'Não há disciplinas cadastradas'
        else:
            str = ''
            for disc in self.listaDisciplinas:
                str += '____________________________________________________________\n'
                str += 'Código: ' + disc.getCodigo() + '\n'
                str += 'Nome: ' + disc.getNome() + '\n'
                str += 'Carga horária: ' + disc.getCargaHoraria() + '\n'
                str += '____________________________________________________________\n'
        
        self.limiteMost = LimiteMostraDisciplinas(str)

    def insereHandler(self, event):
        try:
            if len(self.limiteIns.inputCode.get()) == 0 or len(self.limiteIns.inputNome.get()) == 0 or len(self.limiteIns.inputCarga.get()) == 0:
                raise PreenchaTudo()
            if not self.limiteIns.inputCarga.get().isdigit():
                raise CargaInvalida()
            if self.limiteIns.inputNome.get().isdigit() == True or self.isNumber(self.limiteIns.inputNome.get()) == True:
                raise NomeIsNumero()
            if len(self.limiteIns.inputNome.get()) < 3:
                raise NomeInvalido()
            if len(self.limiteIns.inputCode.get().split(' ')) >= 2:
                raise CodeInvalido()
            for disc in self.listaDisciplinas:
                if disc.getCodigo() == self.limiteIns.inputCode.get() and disc.getNome() == self.limiteIns.inputNome.get():
                    raise Nome_Code_Repetido()
                if disc.getNome() == self.limiteIns.inputNome.get():
                    raise NomeRepetido()
                if disc.getCodigo() == self.limiteIns.inputCode.get():
                    raise CodeRepetido()
                
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except CargaInvalida:
            str = """Carga horária inválida! Digite um número inteiro.
            Exemplos: '64', '80', ..."""
            self.mensagem('Erro', str)
            self.limiteIns.inputCarga.delete(0, len(self.limiteIns.inputCarga.get()))
        except NomeIsNumero:
            str = "Nome inválido! Lembre-se: Seu nome não pode ser um número."
            self.mensagem('Erro', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except NomeInvalido:
            str = "Nome inválido!"
            str += "\nUm nome não pode ser tão pequeno assim a ponto de ter só uma ou duas letras."
            self.mensagem('Erro', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except CodeInvalido:
            self.mensagem('Erro', """Seu código não pode conter espaços!
        Exemplos: 'COM110', 'CC01', '12345', 'ECO15' ...""")
            self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
        except Nome_Code_Repetido:
            self.mensagem('Cadastro não permitido', "Esta disciplina já foi cadastrada!")
            self.ClearHandler(event)
        except NomeRepetido:
            str = ("Já existe uma disciplina com o nome '{}'!".format(self.limiteIns.inputNome.get()))
            self.mensagem('Cadastro não permitido', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except CodeRepetido:
            str = ("O código '{}' já está em uso para outra disciplina!".format(self.limiteIns.inputCode.get()))
            self.mensagem('Cadastro não permitido', str)
            self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
        
        else:
            Code = self.limiteIns.inputCode.get()
            nome = self.limiteIns.inputNome.get()
            cargaHora = self.limiteIns.inputCarga.get()
            disciplina = Disciplina(Code, nome, cargaHora)
            self.listaDisciplinas.append(disciplina)
            self.mensagem('Sucesso', 'Disciplina cadastrada com sucesso')
            self.ClearHandler(event)
    
    def ClearHandler(self, event):
        self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        self.limiteIns.inputCarga.delete(0, len(self.limiteIns.inputCarga.get()))
    
    def concluiHandler(self, event):
        self.limiteIns.destroy()