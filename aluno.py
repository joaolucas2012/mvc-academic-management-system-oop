import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os.path
import pickle

#Exceptions de tratamento
class PreenchaTudo(Exception):
    pass

class AlunoJaCadastrado(Exception):
    pass

class MatricRepetida(Exception):
    pass

class NomeInvalido(Exception):
    pass

class NomeIsNumero(Exception):
    pass

class NroInvalido(Exception):
    pass

class Aluno:
    #Construtor
    def __init__(self, nome, nroMatric, curso):
        self.__nome = nome
        self.__nroMatric = nroMatric
        self.__curso = curso

        #O aluno possui uma lista com os cursos cujas disciplinas ele cursa
        #E uma lista para seus históricos de disciplinas cursadas
        self.__disciplinasObrigatorias = []
        self.__horasObrigatorias = 0
        self.__disciplinasEletivas = []
        self.__horasEletivas = 0
        self.__historico = []

    def getNome(self):
        return self.__nome

    def getNroMatric(self):
        return self.__nroMatric
    
    def getCurso(self):
        return self.__curso
    
    def getDisciplinasObrigatorias(self):
        return self.__disciplinasObrigatorias
    
    def getHorasObgt(self):
        return self.__horasObrigatorias
    
    def getDisciplinasEletivas(self):
        return self.__disciplinasEletivas
    
    def getHorasEltv(self):
        return self.__horasEletivas
    
    def getHistorico(self):
        return self.__historico
    
    def addDisciplinaObrigatoria(self, disciplina):
        #Aqui, uma disciplina obrigatoria pode ser adicionada ao aluno
        self.__horasObrigatorias += int(disciplina.getCargaHoraria())
        self.__disciplinasObrigatorias.append(disciplina)
    
    def addDisciplinaEletiva(self, disciplina):
        #Aqui, uma disciplina eletiva pode ser adicionada ao aluno
        self.__horasEletivas += int(disciplina.getCargaHoraria())
        self.__disciplinasEletivas.append(disciplina)
    
    def addHistorico(self, historico):
        #Aqui um novo registro de historico pode ser adicionado ao aluno
        self.__historico.append(historico)

class LimiteInsereAlunos(tk.Toplevel):
    def __init__(self, controle):
        
        tk.Toplevel.__init__(self)
        self.geometry('250x100')
        self.title("Inserir aluno")
        self.controle = controle

        self.frameNome = tk.Frame(self)
        self.frameNroMatric = tk.Frame(self)
        self.frameCurso = tk.Frame(self)
        self.frameButtons = tk.Frame(self)
        self.frameNome.pack()
        self.frameNroMatric.pack()
        self.frameCurso.pack()
        self.frameButtons.pack()

        self.labelNome = tk.Label(self.frameNome, text = 'Nome:         ')
        self.labelNro = tk.Label(self.frameNroMatric, text = 'Nro Matric: ')
        self.labelCurso = tk.Label(self.frameCurso, text = 'Curso:         ')
        self.labelNome.pack(side = 'left')
        self.labelNro.pack(side = 'left')
        self.labelCurso.pack(side = 'left')

        self.inputNome = tk.Entry(self.frameNome, width = 20)
        self.inputNro = tk.Entry(self.frameNroMatric, width = 20)
        self.escolhaCombo = tk.StringVar()
        self.inputCurso = ttk.Combobox(self.frameCurso, width = 20)
        listaCodCursos = self.controle.CtrlPrincipal.ctrlCurso.getCodListaCursos()
        self.inputCurso['values'] = listaCodCursos
        self.inputNome.pack(side = 'left')
        self.inputNro.pack(side = 'left')
        self.inputCurso.pack(side = 'left')

        self.buttonInserir = tk.Button(self.frameButtons, text = 'Inserir', font = ('Negrito', 9))
        self.buttonInserir.pack(side = 'left')
        self.buttonInserir.bind("<Button>", controle.insereHandler)

        self.buttonClear = tk.Button(self.frameButtons, text = 'Limpar', font = ('Negrito', 9))
        self.buttonClear.pack(side = 'left')
        self.buttonClear.bind("<Button>", controle.ClearHandler)

        self.buttonConcluido = tk.Button(self.frameButtons, text = 'Concuído', font = ('Negrito', 9))
        self.buttonConcluido.pack(side = 'left')
        self.buttonConcluido.bind("<Button>", controle.ConcluidoHandler)

class LimiteMostraAlunos(tk.Toplevel):
    def __init__(self, controle, str):
        self.controle = controle
        self.controle.mensagem('Alunos cadastrados', str)

class CtrlAluno():
    def __init__(self, controlePrincipal):
        self.CtrlPrincipal = controlePrincipal

        if not os.path.isfile("alunos.pickle"):
            self.listaAlunos = []
        else:
            with open("alunos.pickle", "rb") as f:
                self.listaAlunos = pickle.load(f)
    
    def salvaAlunos(self):
        if len(self.listaAlunos) != 0:
            with open("alunos.pickle", "wb") as f:
                pickle.dump(self.listaAlunos, f)
    
    def mensagem(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
    
    def retornaTamanhoListaAlunos(self):
        tamanho = len(self.listaAlunos)
        return tamanho
    
    def isNumber(self, number):
        try:
            if number.isdigit() == True:
                return True
            float(number)
            return True
        except ValueError:
            return False
    
    def printHistoricoDiscObgt(self, aluno):
        str = ''
        if len(aluno.getDisciplinasObrigatorias()) == 0:
            str += ('\nO aluno ainda não cursou disciplinas obrigatórias')
            str += ('\n\nO aluno não possui carga horária cadastrada para disciplinas obrigatórias')
        else:
            str += ('\nDISCIPLINAS OBRIGATÓRIAS CURSADAS: \n')
            for hist in aluno.getHistorico():
                for disciplina in aluno.getDisciplinasObrigatorias():
                    if hist.getDisciplina().getCodigo() == disciplina.getCodigo():
                        str += '\n' + hist.getAno() + '.' + hist.getSemestre() + ' - ' + hist.getDisciplina().getCodigo() + ': ' + hist.getDisciplina().getNome() + '\n'
                        str += "Carga horária: " + hist.getDisciplina().getCargaHoraria() + '\n'
                        if float(hist.getNota()) >= 6:
                            str += """Situação: Aprovado\n"""
                        else:
                            str += """Situação: Reprovado"""            
        str += ("""\n\nCARGA HORÁRIA TOTAL: {}\n\n""".format(aluno.getHorasObgt()))
        titulo = ('Histórico acadêmico de {}'.format(aluno.getNome()))
        self.mensagem(titulo, str)

    def printHistoricoDiscEltv(self, aluno):
        str = ''
        if len(aluno.getDisciplinasEletivas()) == 0:
            str += ('\nO aluno ainda não cursou disciplinas eletivas')
            str += ('\n\nO aluno não possui carga horária cadastrada para disciplinas eletivas')
        else:
            str += ('\nDISCIPLINAS ELETIVAS CURSADAS:\n')
            for hist in aluno.getHistorico():
                for disciplina in aluno.getDisciplinasEletivas():
                    if hist.getDisciplina().getCodigo() == disciplina.getCodigo():
                        str += '\n' + hist.getAno() + '.' + hist.getSemestre() + ' - ' + hist.getDisciplina().getCodigo() + ': ' + hist.getDisciplina().getNome() + '\n'
                        str += "Carga horária: " + hist.getDisciplina().getCargaHoraria() + '\n'
                        if float(hist.getNota()) >= 6:
                            str += """Situação: Aprovado\n"""
                        else:
                            str += """Situação: Reprovado"""
        str += ("""\n\nCARGA HORÁRIA TOTAL: {}\n\n""".format(aluno.getHorasEltv()))
        titulo = ('Histórico acadêmico de {}'.format(aluno.getNome()))
        self.mensagem(titulo, str)
    
    def getAluno(self, NomeOuNroMatric):
        aluRet = None
        for aluno in self.listaAlunos:
            if aluno.getNroMatric() == NomeOuNroMatric:
                aluRet = aluno
            if aluno.getNome() == NomeOuNroMatric:
                aluRet = aluno
        return aluRet
    
    def getDiscGradeAluno(self, alunoRef):
        listaDiscGradeAluno = []
        listaDiscGradeAluno = alunoRef.getCurso().getGrade().getDisciplina()
        return listaDiscGradeAluno
    
    def insereAluno(self):
        self.limiteIns = LimiteInsereAlunos(self)
    
    def mostraAlunos(self):
        if len(self.listaAlunos) == 0:
            str = 'Não há alunos cadastrados'
        else:
            str = ''
            for aluno in self.listaAlunos:
                str+= '\nNro de Matrícula: ' + aluno.getNroMatric() 
                str+= '\nNome: ' + aluno.getNome()  
                str+= '\nCurso: ' + aluno.getCurso().getNome()
                str+= '\n--------------------------------------------'
        self.limiteLista = LimiteMostraAlunos(self, str)

    def insereHandler(self, event):
        try:
            if len(self.limiteIns.inputNome.get()) == 0 or len(self.limiteIns.inputNro.get()) == 0 or len(self.limiteIns.inputCurso.get()) == 0:
                raise PreenchaTudo()
            if self.isNumber(self.limiteIns.inputNome.get()) == True:
                raise NomeIsNumero()
            if len(self.limiteIns.inputNome.get()) < 2:
                raise NomeInvalido()
            if not self.limiteIns.inputNro.get().isdigit() or len(self.limiteIns.inputNro.get().split(' ')) >= 2:
                raise NroInvalido()
            for aluno in self.listaAlunos:
                if aluno.getNome() == self.limiteIns.inputNome.get() and aluno.getNroMatric() == self.limiteIns.inputNro.get() and aluno.getCurso() == self.limiteIns.inputCurso.get():
                    raise AlunoJaCadastrado()
                if aluno.getNroMatric() == self.limiteIns.inputNro.get():
                    raise MatricRepetida()
        except PreenchaTudo:
            self.mensagem("Cadastro não permitido", "Preencha todos os campos!")
        except NomeIsNumero:
            str = "Nome inválido! Lembre-se: Seu nome não pode ser um número."
            self.mensagem('Erro', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except NomeInvalido:
            str = "Nome inválido!"
            str += "\nUm nome não pode ser tão pequeno assim a ponto de ter só uma letra."
            self.mensagem('Erro', str)
            self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        except NroInvalido:
            str = "Número inválido! Digite um número inteiro sem conter espaços."
            str += "\nExemplo: '2019000000'."
            self.mensagem('Erro', str)
            self.limiteIns.inputNro.delete(0, len(self.limiteIns.inputNro.get()))
        except AlunoJaCadastrado:
            self.mensagem("Cadastro não permitido", "Este aluno já foi cadastrado!")
            self.ClearHandler(event)
        except MatricRepetida:
            self.mensagem("Cadastro não permitido", "Já existe um aluno com este número de matrícula!")
            self.limiteIns.inputNro.delete(0, len(self.limiteIns.inputNro.get()))
        else:
            Nome = self.limiteIns.inputNome.get()
            Nro = self.limiteIns.inputNro.get()
            cursoSel = self.limiteIns.inputCurso.get()
            curso = self.CtrlPrincipal.ctrlCurso.getCursoPorCode(cursoSel)
            aluno = Aluno(Nome, Nro, curso)
            self.listaAlunos.append(aluno)
            self.mensagem('Sucesso', 'Aluno Cadastrado!')
            self.ClearHandler(event)

    def ClearHandler(self, event):
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))
        self.limiteIns.inputNro.delete(0, len(self.limiteIns.inputNro.get()))
        self.limiteIns.inputCurso.delete(0, len(self.limiteIns.inputCurso.get()))
    
    def ConcluidoHandler(self, event):
        self.limiteIns.destroy()