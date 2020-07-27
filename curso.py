import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os.path
import pickle

#Exceptions de tratamento
class PreenchaTudo(Exception):
    pass

class NomeDuplicado(Exception):
    pass

class NomeInvalido(Exception):
    pass

class CodeDuplicado(Exception):
    pass

class CursoJaExiste(Exception):
    pass

class CodeInvalido(Exception):
    pass

class NomeIsNumero(Exception):
    pass

class Curso:
    #Construtor
    def __init__(self, nome, codigo, grade):
        self.__nome = nome 
        self.__codigo = codigo
        #Cada curso possui exatamente uma grade
        self.__grade = grade

    def getNome(self):
        return self.__nome
    
    def getCodigo(self):
        return self.__codigo
    
    def getGrade(self):
        return self.__grade

class LimiteInsereCursos(tk.Toplevel):
    def __init__(self, controle, listaGrades):
        
        tk.Toplevel.__init__(self)
        self.geometry("250x100")
        self.title('Inserir curso')
        self.controle = controle

        self.frameNome = tk.Frame(self)
        self.frameNome.pack()
        self.frameCode = tk.Frame(self)
        self.frameCode.pack()
        self.frameComboBox = tk.Frame(self)
        self.frameComboBox.pack()
        self.frameButtons = tk.Frame(self)
        self.frameButtons.pack()

        self.labelNome = tk.Label(self.frameNome, text = 'Nome:  ')
        self.labelNome.pack(side = 'left')
        self.inputNome = tk.Entry(self.frameNome, width = 30)
        self.inputNome.pack(side = 'left')

        self.labelCode = tk.Label(self.frameCode, text = 'Código: ')
        self.labelCode.pack(side = 'left')
        self.inputCode = tk.Entry(self.frameCode, width = 30)
        self.inputCode.pack(side = 'left')

        self.labelGradesCurso = tk.Label(self.frameComboBox, text = 'Escolha uma grade para compô-lo: ')
        self.labelGradesCurso.pack(side = 'left')
        self.escolhaCombo = tk.StringVar()
        self.comboboxGrades = ttk.Combobox(self.frameComboBox, width = 5, textvariable = self.escolhaCombo)
        self.comboboxGrades.pack(side = 'left')
        self.comboboxGrades['values'] = listaGrades

        self.buttonInsere = tk.Button(self.frameButtons, text = 'Inserir', font = ('Negrito', 9))
        self.buttonInsere.pack(side = 'left')
        self.buttonInsere.bind("<Button>", controle.insereHandler)

        self.buttonClear = tk.Button(self.frameButtons, text = 'Limpar', font = ('Negrito', 9))
        self.buttonClear.pack(side = 'left')
        self.buttonClear.bind("<Button>", controle.ClearHandler)

        self.buttonSair = tk.Button(self.frameButtons, text = 'Concluído', font = ('Negrito', 9))
        self.buttonSair.pack(side = 'left')
        self.buttonSair.bind("<Button>", controle.exitHandler)

class LimiteMostraCursos():
    def __init__(self, str):
        messagebox.showinfo('Cursos cadastrados', str)

class CtrlCurso():
    def __init__(self, controlePrincipal):
        self.CtrlPrincipal = controlePrincipal

        if not os.path.isfile("cursos.pickle"):
            self.listaCursos = []
        else:
            with open("cursos.pickle", "rb") as f:
                self.listaCursos = pickle.load(f)
    
    def salvaCursos(self):
        if len(self.listaCursos) != 0:
            with open("cursos.pickle", "wb") as f:
                pickle.dump(self.listaCursos, f)
    
    def mensagem(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
    
    def retornaTamanhoListaCursos(self):
        tamanho = len(self.listaCursos)
        return tamanho
    
    def getCursoPorCode(self, code):
        cursoRet = None
        for curso in self.listaCursos:
            if code == curso.getCodigo() or code == curso.getNome():
                cursoRet = curso
        return cursoRet
    
    def getGradePorCurso(self, cursoRef):
        curso = cursoRef
        gradeRet = None
        for cur in self.listaCursos:
            if curso.getCodigo() == cur.getCodigo():
                gradeRet = curso.getGrade()
        return gradeRet

    def getListaCursos(self):
        return self.listaCursos
    
    def getCodListaCursos(self):
        listaCodCursos = []
        for curso in self.listaCursos:
            listaCodCursos.append(curso.getCodigo())
        return listaCodCursos
    
    def isNumber(self, number):
        try:
            if number.isdigit() == True:
                return True
            float(number)
            return True
        except ValueError:
            return False
    
    def insereCurso(self):
        listaGrades = self.CtrlPrincipal.ctrlGrade.getListaCodGrades()
        self.limiteIns = LimiteInsereCursos(self, listaGrades)
    
    def mostraCursos(self):
        str = ''
        if len(self.listaCursos) == 0:
            str = 'Não há cursos cadastrados'
        else:
            listaGrades = self.CtrlPrincipal.ctrlGrade.getListaGrades()
            for curso in self.listaCursos:
                str += '\n-------------------------------------------'
                str += '\nNome: ' + curso.getNome()
                str += '\nCódigo: ' + curso.getCodigo()    
                for grade in listaGrades:
                    if curso.getGrade().getCodigo() == grade.getCodigo():
                        str += '\nGrade: ' + grade.getCodigo() + ' - ' + grade.getAno() + '.' + grade.getSemestre() 
                str += '\n-------------------------------------------'

        self.limiteMost = LimiteMostraCursos(str)
    
    def insereHandler(self, event):
        try:
            if len(self.limiteIns.inputCode.get()) == 0 or len(self.limiteIns.inputNome.get()) == 0 or len(self.limiteIns.escolhaCombo.get()) == 0:
                raise PreenchaTudo()
            if len(self.limiteIns.inputCode.get()) > 5 or len(self.limiteIns.inputCode.get().split(' ')) >= 2:
                raise CodeInvalido()
            if self.isNumber(self.limiteIns.inputNome.get()) == True:
                raise NomeIsNumero()
            if len(self.limiteIns.inputNome.get()) < 2:
                raise NomeInvalido()
            else:
                for curso in self.listaCursos:
                    if self.limiteIns.inputCode.get() == curso.getCodigo() and self.limiteIns.inputNome.get() == curso.getNome() and self.limiteIns.escolhaCombo.get() == curso.getGrade():
                        raise CursoJaExiste()
                    if self.limiteIns.inputNome.get() == curso.getNome():
                        raise NomeDuplicado()
                    if self.limiteIns.inputCode.get() == curso.getCodigo():
                        raise CodeDuplicado()
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except CodeInvalido:
            self.mensagem('Erro', """Seu código deve conter no máximo 5 caracteres e não pode conter espaços!
        Exemplos: 'SIN', 'CC01', '12345', 'ECO15' ...""")
            self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
        except NomeIsNumero:
            str = "Nome inválido! Lembre-se: Seu nome não pode ser um número."
            self.mensagem('Erro', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except NomeInvalido:
            str = "Nome inválido!"
            str += "\nUm nome não pode ser tão pequeno assim a ponto de ter só 2 letras."
            self.mensagem('Erro', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except CursoJaExiste:
            self.mensagem('Erro', 'Este curso já foi cadastrado!')
        except NomeDuplicado:
            self.mensagem('Erro', 'Já existe um curso com este nome!')
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except CodeDuplicado:
            self.mensagem('Erro', 'Já existe um curso com este código!')
            self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
        
        else:
            nome = self.limiteIns.inputNome.get()
            code = self.limiteIns.inputCode.get()
            gradeSel = self.limiteIns.escolhaCombo.get()
            grade = self.CtrlPrincipal.ctrlGrade.getGradePorCode(gradeSel)
            curso = Curso(nome, code, grade)
            self.listaCursos.append(curso)
            self.mensagem('Inserção realizada', 'Curso cadastrado com sucesso!')
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
            self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
    
    def ClearHandler(self, event):
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
    
    def exitHandler(self, event):
        self.limiteIns.destroy()
