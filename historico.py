import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os.path
import pickle

#Exceptions de tratamento
class CampoVazio(Exception):
    pass

class AnoInvalido(Exception):
    pass

class VeiodoPassado(Exception):
    pass

class NotaInvalida(Exception):
    pass

class DiscJaFoiCursada(Exception):
    pass

class OutraTentativa(Exception):
    pass

class Historico:
    #Construtor
    def __init__(self, aluno, disciplina, ano, semestre, nota):
        self.__aluno = aluno
        self.__disciplina = disciplina
        self.__ano = ano
        self.__semest = semestre
        self.__nota = nota
    
    def getAluno(self):
        return self.__aluno
    
    def getDisciplina(self):
        return self.__disciplina

    def getAno(self):
        return self.__ano
    
    def getSemestre(self):
        return self.__semest
    
    def getNota(self):
        return self.__nota

class LimiteInsereHistorico(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('500x100')
        self.title('Buscar Histórico do Aluno')
        self.controle = controle

        self.frameAluno = tk.Frame(self)
        self.frameAluno.pack()
        self.labelNomeOuNro = tk.Label(self.frameAluno, text = 'Informe um nome ou Nro de Matric. do aluno: ')
        self.labelNomeOuNro.pack(side = 'left')
        self.inputNomeOuNro = tk.Entry(self.frameAluno, width = 20)
        self.inputNomeOuNro.pack(side = 'left')

        self.frameButton = tk.Button(self)
        self.frameButton.pack()
        
        self.buttonBuscar = tk.Button(self.frameButton, text = 'Buscar', font = ('Negrito', 9))
        self.buttonBuscar.pack(side = 'left')
        self.buttonBuscar.bind("<Button>", controle.consultaHandler)

        self.buttonSair = tk.Button(self.frameButton, text = 'Sair', font = ('Negrito', 9))
        self.buttonSair.pack(side = 'left')
        self.buttonSair.bind("<Button>", controle.exitHandler)

class LimiteMostraHistorico(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('500x100')
        self.title('Buscar Histórico do Aluno')
        self.controle = controle

        self.frameAluno = tk.Frame(self)
        self.frameAluno.pack()
        self.labelNomeOuNro = tk.Label(self.frameAluno, text = 'Informe um nome ou Nro de Matric. do aluno: ')
        self.labelNomeOuNro.pack(side = 'left')
        self.inputNomeOuNro = tk.Entry(self.frameAluno, width = 20)
        self.inputNomeOuNro.pack(side = 'left')

        self.frameButton = tk.Button(self)
        self.frameButton.pack()
        
        self.buttonBuscar = tk.Button(self.frameButton, text = 'Buscar', font = ('Negrito', 9))
        self.buttonBuscar.pack(side = 'left')
        self.buttonBuscar.bind("<Button>", controle.MostraHandler)

        self.buttonSair = tk.Button(self.frameButton, text = 'Sair', font = ('Negrito', 9))
        self.buttonSair.pack(side = 'left')
        self.buttonSair.bind("<Button>", controle.exitMostHandler)

class LimiteJanelaHistorico(tk.Toplevel):
    def __init__(self, controle, aluno):

        tk.Toplevel.__init__(self)
        self.geometry('400x200')
        self.title('Inserir Histórico para {}'.format(aluno.getNome()))
        self.controle = controle
        self.aluno = aluno

        self.frameTitle = tk.Frame(self)
        self.frameTitle.pack()
        self.labelTitle = tk.Label(self.frameTitle, text = """Informe os dados abaixo:
        ------------------------------------------------------------------------------------------------------
        """ , font = ('Arial', 10))
        self.labelTitle.pack()

        self.frameDisc = tk.Frame(self)
        self.frameDisc.pack()
        self.labelDisc = tk.Label(self.frameDisc, text = 'Disciplina cursada:       ')
        self.labelDisc.pack(side = 'left')
        self.escolhaCombo = tk.StringVar()
        self.comboboxDisc = ttk.Combobox(self.frameDisc, width = 10, textvariable = self.escolhaCombo)
        self.comboboxDisc.pack(side = 'left')
        listaCodDisc = self.controle.CtrlPrincipal.ctrlDisciplina.getListaCodDisciplinas()
        self.comboboxDisc['values'] = listaCodDisc

        self.frameAno = tk.Frame(self)
        self.frameAno.pack()
        self.labelAno = tk.Label(self.frameAno, text = 'Ano em que foi cursada:   ')
        self.labelAno.pack(side = 'left')
        self.inputAno = tk.Entry(self.frameAno, width = 10)
        self.inputAno.pack(side = 'left')

        self.frameSemest = tk.Frame(self)
        self.frameSemest.pack()
        self.labelSemest = tk.Label(self.frameSemest, text = 'Semestre em que foi cursada: ')
        self.labelSemest.pack(side = 'left')
        listaSemest = ['1', '2']
        self.escolhaComboSemest = tk.StringVar()
        self.comboSemest = ttk.Combobox(self.frameSemest, width = 4, textvariable = self.escolhaComboSemest)
        self.comboSemest.pack(side = 'left')
        self.comboSemest['values'] = listaSemest

        self.frameNota = tk.Frame(self)
        self.frameNota.pack()
        self.LabelNota = tk.Label(self.frameNota, text = 'Nota final obtida:                 ')
        self.LabelNota.pack(side = 'left')
        self.inputNota = tk.Entry(self.frameNota, width = 10)
        self.inputNota.pack(side = 'left')

        self.frameButtons = tk.Frame(self)
        self.frameButtons.pack()
        
        self.buttonInsere = tk.Button(self.frameButtons, text = 'Inserir', font = ('Negrito', 9))
        self.buttonInsere.pack(side = 'left')
        self.buttonInsere.bind("<Button>", controle.insereHandler)

        self.buttonClear = tk.Button(self.frameButtons, text = 'Limpar', font = ('Negrito', 9))
        self.buttonClear.pack(side = 'left')
        self.buttonClear.bind("<Button>", controle.clearHandler)

        self.buttonExit = tk.Button(self.frameButtons, text = 'Sair', font = ('Negrito', 9))
        self.buttonExit.pack(side = 'left')
        self.buttonExit.bind("<Button>", controle.SairHandler)

    def returnAluno(self):
        return self.aluno

class LimiteDesejaInserirMaisHistoricos(tk.Toplevel):
    def __init__(self, controle, aluno):

        tk.Toplevel.__init__(self)
        self.geometry('500x100')
        self.controle = controle
        self.aluno = aluno
        self.title('Continuar inserções para {}'.format(self.aluno.getNome()))

        self.framePergunta = tk.Frame(self)
        self.framePergunta.pack()
        self.labelPergunta = tk.Label(self.framePergunta, text = 'Deseja inserir outro histórico a este aluno?', font = ('Negrito'))
        self.labelPergunta.pack()
        
        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        self.buttonYes = tk.Button(self.frameButton, text = 'Sim', font = ('Negrito', 9))
        self.buttonYes.pack(side = 'left')
        self.buttonYes.bind("<Button>", controle.YesHandler)

        self.buttonNot = tk.Button(self.frameButton, text = 'Não', font = ('Negrito', 9))
        self.buttonNot.pack(side = 'left')
        self.buttonNot.bind("<Button>", controle.NotHandler)

    def retornaAluno(self):
        return self.aluno

class LimiteHistoricoDisc(tk.Toplevel):
    def __init__(self, controle, aluno):

        tk.Toplevel.__init__(self)
        self.geometry('500x100')
        self.title('Mostrar Histórico para {}'.format(aluno.getNome()))
        self.controle = controle
        self.aluno = aluno

        self.frameTitle = tk.Frame(self)
        self.frameTitle.pack()
        self.labelTitle = tk.Label(self.frameTitle, text = "Escolha o histórico desejado:\n" , font = ('Arial', 10))
        self.labelTitle.pack()

        self.frameButtons1 = tk.Frame(self)
        self.frameButtons1.pack()
        self.frameButton2 = tk.Frame(self)
        self.frameButton2.pack()

        self.buttonDiscObgt = tk.Button(self.frameButtons1, text = 'Disciplinas Obrigatórias', font = ('Negrito', 9))
        self.buttonDiscObgt.pack(side = 'left')
        self.buttonDiscObgt.bind("<Button>", controle.discObgtHandler)

        self.buttonDiscEltv = tk.Button(self.frameButtons1, text = 'Disciplinas Eletivas', font = ('Negrito', 9))
        self.buttonDiscEltv.pack(side = 'left')
        self.buttonDiscEltv.bind("<Button>", controle.discEltvHandler)

        self.buttonSair = tk.Button(self.frameButton2, text = 'Sair', font = ('Negrito', 9))
        self.buttonSair.pack()
        self.buttonSair.bind("<Button>", controle.SaindoHandler)
    
    def retornaAluno(self):
        return self.aluno

class CtrlHistorico():
    def __init__(self, controlePrincipal):
        self.CtrlPrincipal = controlePrincipal
    
    def mensagem(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
    
    def insereHistorico(self):
        tamanho = self.CtrlPrincipal.ctrlAluno.retornaTamanhoListaAlunos()
        if tamanho == 0:
            self.mensagem('Erro ao inserir histórico','Não há alunos cadastrados para inserção de históricos')
        else:
            self.limiteIns = LimiteInsereHistorico(self) 
    
    def mostraHistoricos(self):
        tamanho = self.CtrlPrincipal.ctrlAluno.retornaTamanhoListaAlunos()
        if tamanho == 0:
            self.mensagem('Erro ao acessar histórico','Não há históricos cadastrados')
        else:
            self.limiteMost = LimiteMostraHistorico(self)
    
    def consultaHandler(self, event):
        try:
            if len(self.limiteIns.inputNomeOuNro.get()) == 0:
                raise CampoVazio()
        except CampoVazio:
            self.mensagem('Erro', 'Digite um nome ou Nro de Matrícula!')
            
        else:
            NomeOuMatric = self.limiteIns.inputNomeOuNro.get()
            aluno = self.CtrlPrincipal.ctrlAluno.getAluno(NomeOuMatric)
            if aluno == None:
                str = ("Nenhum aluno possui a matrícula ou nome igual a '{}' ".format(NomeOuMatric))
                self.mensagem('Aluno não encontrado', str)
                self.limiteIns.inputNomeOuNro.delete(0, len(self.limiteIns.inputNomeOuNro.get()))
            else:
                self.janelaHistorico = LimiteJanelaHistorico(self, aluno)
                self.limiteIns.destroy()
                  
    def isNumber(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False
    
    def isHistoricoRepetido(self, aluno, CodDisc, semestre, nota):
        alu = aluno
        nota = nota
        for hist in alu.getHistorico():
            if CodDisc == hist.getDisciplina().getCodigo() and semestre == hist.getSemestre():
                return True
            if CodDisc == hist.getDisciplina().getCodigo() and semestre != hist.getSemestre():
                if hist.getNota() < 6 and nota >= 6:
                    return False
            else:
                return False

    def insereHandler(self, event):
        try:
            if len(self.janelaHistorico.escolhaCombo.get()) == 0 or len(self.janelaHistorico.inputAno.get()) == 0 or len(self.janelaHistorico.escolhaComboSemest.get()) == 0 or len(self.janelaHistorico.inputNota.get()) == 0:
                raise CampoVazio() 
            if not self.janelaHistorico.inputAno.get().isdigit() or len(self.janelaHistorico.inputAno.get()) != 4 or len(self.janelaHistorico.inputAno.get().split(' ')) >= 2:
                raise AnoInvalido()
            if float(self.janelaHistorico.inputAno.get()) < 1950:
                raise VeiodoPassado()
            if self.isNumber(self.janelaHistorico.inputNota.get()) != True or len(self.janelaHistorico.inputNota.get().split(' ')) >= 2:
                raise NotaInvalida()
            if float(self.janelaHistorico.inputNota.get()) > 10 or float(self.janelaHistorico.inputNota.get()) < 0 or len(self.janelaHistorico.inputNota.get()) > 3:
                raise NotaInvalida()
            if self.isHistoricoRepetido(self.janelaHistorico.returnAluno(), self.janelaHistorico.escolhaCombo.get(), self.janelaHistorico.escolhaComboSemest.get(), self.janelaHistorico.inputNota.get()) == True:
                raise DiscJaFoiCursada()  
        except CampoVazio:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except AnoInvalido:
            self.mensagem('Erro', 'Ano inválido!')
            self.janelaHistorico.inputAno.delete(0, len(self.janelaHistorico.inputAno.get()))
        except VeiodoPassado:
            self.mensagem('Algo errado', 'Para que registrar um histórico tão antigo?')
            self.janelaHistorico.inputAno.delete(0, len(self.janelaHistorico.inputAno.get()))
        except NotaInvalida:
            str = 'Nota inválida!\n'
            str += 'Digite um número de 0 a 10, com no máximo um algarismo depois do ponto (que representa a vírgula).\n'
            str += "Exemplos: '10', '9.7', '2', '3.5' ..."
            self.mensagem('Erro', str)
            self.janelaHistorico.inputNota.delete(0, len(self.janelaHistorico.inputNota.get()))
        except DiscJaFoiCursada:
            self.mensagem('Histórico já inserido', 'Esta disciplina já foi cursada por este aluno neste mesmo semestre!')

        else:
            discSel = self.janelaHistorico.escolhaCombo.get()
            discip = self.CtrlPrincipal.ctrlDisciplina.getDisciplina(discSel)
            aluno = self.janelaHistorico.aluno
            ano = self.janelaHistorico.inputAno.get()
            semestre = self.janelaHistorico.escolhaComboSemest.get()
            nota = self.janelaHistorico.inputNota.get()
            historico = Historico(aluno, discip, ano, semestre, nota)
            listaDiscGradeAluno = []
            listaDiscGradeAluno = self.CtrlPrincipal.ctrlAluno.getDiscGradeAluno(aluno)
            try:
                for discGrade in listaDiscGradeAluno:
                    if historico.getDisciplina().getCodigo() == discGrade.getDisciplinaGrade().getCodigo():
                        aluno.addDisciplinaObrigatoria(historico.getDisciplina())
                        aluno.addHistorico(historico)
                        self.mensagem('Sucesso', 'Histórico adicionado!') 
                        self.limiteDesejaIns = LimiteDesejaInserirMaisHistoricos(self, aluno)
                        self.janelaHistorico.destroy()
                    else:
                        raise OutraTentativa()
            except OutraTentativa:
                for grad in self.CtrlPrincipal.ctrlGrade.getListaGrades():
                    if grad.getCodigo() != aluno.getCurso().getGrade().getCodigo():
                        for disc in grad.getDisciplina():
                            if disc.getDisciplinaGrade().getCodigo() == historico.getDisciplina().getCodigo():
                                aluno.addDisciplinaEletiva(historico.getDisciplina()) 
                                aluno.addHistorico(historico)   
                                self.mensagem('Sucesso', 'Histórico adicionado!')   
                                self.limiteDesejaIns = LimiteDesejaInserirMaisHistoricos(self, aluno)
                                self.janelaHistorico.destroy()
                            else:
                                str = 'Esta disciplina está cadastrada mas ainda não foi inserida em nenhuma grade de nenhum curso!'
                                str += '\nSe a disciplina não está em uma grade ou curso, não pode ser considerada disciplina obrigatória ou eletiva.'
                        self.mensagem('Erro ao inserir histórico', str)           
    
    def MostraHandler(self, event):
        try:
            if len(self.limiteMost.inputNomeOuNro.get()) == 0:
                raise CampoVazio()
        except CampoVazio:
            messagebox.showinfo('Erro', 'Digite um nome ou Nro de Matrícula!')
            
        else:
            NomeOuMatric = self.limiteMost.inputNomeOuNro.get()
            aluno = self.CtrlPrincipal.ctrlAluno.getAluno(NomeOuMatric)
            if aluno == None:
                str = ("Nenhum aluno possui a matrícula ou nome igual a '{}' ".format(NomeOuMatric))
                messagebox.showinfo('Aluno não encontrado', str)
                self.limiteMost.inputNomeOuNro.delete(0, len(self.limiteMost.inputNomeOuNro.get()))
            else:
                self.HistJan = LimiteHistoricoDisc(self, aluno)
                self.limiteMost.destroy()
                
    def exitHandler(self, event):
        self.limiteIns.destroy()
    
    def SairHandler(self, event):
        self.janelaHistorico.destroy()
    
    def exitMostHandler(self, event):
        self.limiteMost.destroy()
    
    def clearHandler(self, event):
        self.janelaHistorico.inputAno.delete(0, len(self.janelaHistorico.inputAno.get()))
        self.janelaHistorico.inputNota.delete(0, len(self.janelaHistorico.inputNota.get()))
    
    def discObgtHandler(self, event):
        aluno = self.HistJan.retornaAluno()
        self.CtrlPrincipal.ctrlAluno.printHistoricoDiscObgt(aluno)

    def discEltvHandler(self, event):
        aluno = self.HistJan.retornaAluno()
        self.CtrlPrincipal.ctrlAluno.printHistoricoDiscEltv(aluno)
    
    def SaindoHandler(self, event):
        self.HistJan.destroy()
    
    def YesHandler(self, event):
        self.limiteDesejaIns.destroy()
        self.janelaHistorico = LimiteJanelaHistorico(self, self.limiteDesejaIns.retornaAluno())

    def NotHandler(self, event):
        self.limiteDesejaIns.destroy()
        self.janelaHistorico.destroy()
        self.limiteIns.destroy()