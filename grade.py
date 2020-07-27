import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os.path
import pickle

#Exceptions de tratamento
class PreenchaTudo(Exception):
    pass

class FaltouAno(Exception):
    pass

class AnoInvalido(Exception):
    pass

class VeioDoPassado(Exception):
    pass

class FaltouCode(Exception):
    pass

class CodeInvalido(Exception):
    pass

class FaltouSemestre(Exception):
    pass

class SemestreInvalido(Exception):
    pass

class SemestreComLetra(Exception):
    pass

class FaltouPeriodo(Exception):
    pass

class PeriodoInvalido(Exception):
    pass

class GradeDuplicada(Exception):
    pass

class GradeNaoExiste(Exception):
    pass

class FaltouDisc(Exception):
    pass

class DiscJaCadastrada(Exception):
    pass

class DiscCadastradaAPeriodoAnterior(Exception):
    pass

class GradeDontHaveThisPeriod(Exception):
    pass

class Grade: 
    #Construtor
    def __init__(self, codigo, ano, semestre):
        self.__codigo = codigo
        self.__ano = ano
        self.__semestre = semestre
    
        #A grade é composta por uma lista de disciplinas
        #Isto se torna uma agregação
        self.__disciplinas = []

    def getCodigo(self):
        return self.__codigo

    def getAno(self):
        return self.__ano
    
    def getSemestre(self):
        return self.__semestre

    def getDisciplina(self):
        return self.__disciplinas
    
    def addDisciplina(self, disciplina):
        self.__disciplinas.append(disciplina)

# Criando uma classe que representa uma disciplina da grade, que possui um período
# Por isto este tipo de disciplina da grade é diferente das disciplinas comuns
class DisciplinaGrade:
    def __init__(self, periodo, disciplina):
        self.__periodo = periodo
        self.__disciplina = disciplina
    
    def getPeriodo(self):
        return self.__periodo
    
    def getDisciplinaGrade(self):
        return self.__disciplina

class LimiteInsereGrade(tk.Toplevel):
    def __init__(self, controle, listaDiscps):

        tk.Toplevel.__init__(self)
        self.geometry("400x100")
        self.title('Inserir Grade')
        self.controle = controle

        self.frameCode = tk.Frame(self)
        self.frameCode.pack()
        self.frameAno = tk.Frame(self)
        self.frameAno.pack()
        self.frameSemest = tk.Frame(self)
        self.frameSemest.pack()
        self.frameButtons = tk.Frame(self)
        self.frameButtons.pack()

        self.labelCode = tk.Label(self.frameCode, text = 'Informe o código:    ')
        self.labelCode.pack(side = 'left')
        self.inputCode = tk.Entry(self.frameCode, width = 20)
        self.inputCode.pack(side = 'left')

        self.labelAno = tk.Label(self.frameAno, text = 'Informe o ano:          ')
        self.labelAno.pack(side = 'left')
        self.inputAno = tk.Entry(self.frameAno, width = 20)
        self.inputAno.pack(side = 'left')

        self.labelSemest = tk.Label(self.frameSemest, text = 'Informe o semestre: ')
        self.labelSemest.pack(side = 'left')
        self.escolhaSemest = tk.StringVar()
        self.comboboxSemest = ttk.Combobox(self.frameSemest, width = 10, textvariable = self.escolhaSemest)
        self.comboboxSemest.pack(side = 'left')
        self.listaSemest = ['1', '2']
        self.comboboxSemest['values'] = self.listaSemest

        self.buttonCria = tk.Button(self.frameButtons, text = 'Inserir disciplinas', font = ('Negrito', 9))
        self.buttonCria.pack(side = 'left')
        self.buttonCria.bind("<Button>", controle.criaGrade)

        self.buttonSair = tk.Button(self.frameButtons, text = 'Sair', font = ('Negrito, 9'))
        self.buttonSair.pack(side = 'left')
        self.buttonSair.bind("<Button>", controle.SaiInsGradHandler)

class LimiteInsereDiscNaGrade(tk.Toplevel):
    def __init__(self, controle, grade):

        tk.Toplevel.__init__(self)
        self.geometry("400x200")
        self.controle = controle
        self.__grade = grade
        self.title('Inserir disciplinas na Grade {}'.format(self.__grade.getCodigo()))

        self.frameDisc = tk.Frame(self)
        self.frameDisc.pack()
        self.framePeriodo = tk.Frame(self)
        self.framePeriodo.pack()
        self.frameButtons = tk.Frame(self)
        self.frameButtons.pack()

        self.labelDisc = tk.Label(self.frameDisc, text = 'Escolha as disciplinas que vão a compor: ')
        self.labelDisc.pack()
        self.escolhaDisc = tk.StringVar()
        self.combodisc = ttk.Combobox(self.frameDisc, width = 10, textvariable = self.escolhaDisc)
        self.combodisc.pack(side = 'top')
        listaCodDisc = []
        for disc in controle.CtrlPrincipal.ctrlDisciplina.getListaDisciplinas():
            listaCodDisc.append(disc.getCodigo())
        self.combodisc['values'] = listaCodDisc

        self.labelPeriodo = tk.Label(self.framePeriodo, text = 'Informe o período em que será inserida:')
        self.labelPeriodo.pack(side = 'top')
        self.escolhaPeriodo = tk.StringVar()
        self.comboPeriodo = ttk.Combobox(self.framePeriodo, width = 10, textvariable = self.escolhaPeriodo)
        listaPeriodo = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.comboPeriodo['values'] = listaPeriodo
        self.comboPeriodo.pack()

        self.buttonInsere = tk.Button(self.frameButtons, text = 'Inserir disciplina')
        self.buttonInsere.pack()
        self.buttonInsere.bind("<Button>", controle.insereDisciplina)

        self.buttonCriaGrade = tk.Button(self.frameButtons, text = 'Criar grade')
        self.buttonCriaGrade.pack()
        self.buttonCriaGrade.bind("<Button>", controle.CriaDefinitivo)
    
    def retornaGrade(self):
        return self.__grade

class LimiteMostraGrades(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('500x100')
        self.title('Buscar Grade por Curso')
        self.controle = controle

        self.frameBusca = tk.Frame(self)
        self.frameBusca.pack()
        self.labelBusca = tk.Label(self.frameBusca, text = 'Informe o código ou o nome do curso: ')
        self.labelBusca.pack(side = 'left')
        self.inputNomeOuCode = tk.Entry(self.frameBusca, width = 20)
        self.inputNomeOuCode.pack(side = 'left')

        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        self.buttonBuscar = tk.Button(self.frameButton, text = 'Buscar', font = ('Negrito', 9))
        self.buttonBuscar.pack(side = 'left')
        self.buttonBuscar.bind("<Button>", controle.BuscarGradeHandler)

        self.buttonSai = tk.Button(self.frameButton, text = 'Sair', font = ('Negrito', 9))
        self.buttonSai.pack(side = 'left')
        self.buttonSai.bind("<Button>", controle.SaiMostGradHandler)

class LimiteShowDiscGrade(tk.Toplevel):
    def __init__(self, controle, grade):

        tk.Toplevel.__init__(self)
        self.geometry('500x100')
        self.title('Buscar grade por curso')
        self.controle = controle
        self.__grade = grade

        self.framePeriod = tk.Frame(self)
        self.framePeriod.pack()
        self.labelPeriod = tk.Label(self.framePeriod, text = 'Informe o período desejado: ')
        self.labelPeriod.pack(side = 'left')
        self.escolhaPeriod = tk.StringVar()
        self.comboperiod = ttk.Combobox(self.framePeriod, width = 10, textvariable = self.escolhaPeriod)
        self.comboperiod.pack(side = 'top')
        listaComboPeriod = []
        for DISC in grade.getDisciplina():
            if not DISC.getPeriodo() in listaComboPeriod:
                listaComboPeriod.append(DISC.getPeriodo())
        self.comboperiod['values'] = listaComboPeriod

        self.frameButton = tk.Frame(self)
        self.frameButton.pack()

        self.buttonShow = tk.Button(self.frameButton, text = 'Mostrar', font = ('Negrito', 9))
        self.buttonShow.pack(side = 'left')
        self.buttonShow.bind("<Button>", controle.MostrarDiscHandler)

        self.buttonSai = tk.Button(self.frameButton, text = 'Sair', font = ('Negrito', 9))
        self.buttonSai.pack(side = 'top')
        self.buttonSai.bind("<Button>", controle.SaiShowDiscHandler)

    def retornaGrad(self):
        return self.__grade
        
class CtrlGrade():
    def __init__(self, controlePrincipal):
        self.CtrlPrincipal = controlePrincipal

        if not os.path.isfile("grades.pickle"):
            self.listaGrades = []
        else:
            with open("grades.pickle", "rb") as f:
                self.listaGrades = pickle.load(f)
    
    def mensagem(self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        
    def salvaGrades(self):
        if len(self.listaGrades) != 0:
            with open("grades.pickle", "wb") as f:
                pickle.dump(self.listaGrades, f)
    
    def getGradePorCode(self, code):
        gradeRet = None
        for grade in self.listaGrades:
            if code == grade.getCodigo():
                gradeRet = grade
        return gradeRet
    
    def getGradePorCurso(self, NomeOuCode):
        gradeRet = None
        Code = NomeOuCode
        curso = self.CtrlPrincipal.ctrlCurso.getCursoPorCode(Code)
        if curso == None:
            str = ("Nenhum curso possui o código ou nome igual a '{}'".format(Code))
            messagebox.showinfo('Curso não encontrado', str)
            self.limiteMost.inputNomeOuCode.delete(0, len(self.limiteMost.inputNomeOuCode.get()))
        else:
            grade = curso.getGrade()
            gradeRet = grade        
        return gradeRet

    def getDiscGrade(self, gradeRef):
        grade = gradeRef
        listaDiscGrade = []
        for grad in self.listaGrades:
            if grade == grad.getCodigo():
                listaDiscGrade = grad.getDisciplina()
        return listaDiscGrade
    
    def getListaGrades(self):
        return self.listaGrades

    def getListaCodGrades(self):
        listaCodGrades = []
        for grade in self.listaGrades:
            listaCodGrades.append(grade.getCodigo())
        return listaCodGrades
    
    def insereGrade(self):
        listaDiscips = self.CtrlPrincipal.ctrlDisciplina.getListaDisciplinas()
        self.limiteIns = LimiteInsereGrade(self, listaDiscips)
    
    def isNumber(self, number):
        try:
            if number.isdigit() == True:
                return True
            float(number)
            return True
        except ValueError:
            return False
    
    def criaGrade(self, event):
        try:
            if len(self.limiteIns.inputCode.get()) == 0 and len(self.limiteIns.inputAno.get()) == 0 and len(self.limiteIns.escolhaSemest.get()) == 0:
                raise PreenchaTudo()
            if len(self.limiteIns.inputCode.get()) == 0:
                raise FaltouCode()
            if len(self.limiteIns.inputAno.get()) == 0:
                raise FaltouAno()
            if len(self.limiteIns.inputAno.get()) != 4 or self.isNumber(self.limiteIns.inputAno.get()) == False:
                raise AnoInvalido()
            if float(self.limiteIns.inputAno.get()) < 1990:
                raise VeioDoPassado()
            if len(self.limiteIns.escolhaSemest.get()) == 0:
                raise FaltouSemestre()
            if self.isNumber(self.limiteIns.escolhaSemest.get()) == False:
                raise SemestreComLetra()
            # if int(self.limiteIns.escolhaSemest.get()) < 1 or int(self.limiteIns.escolhaSemest.get()) < 2:
            #     raise SemestreInvalido()
            if len(self.limiteIns.inputCode.get()) > 5 or len(self.limiteIns.inputCode.get().split(' ')) >= 2:
                raise CodeInvalido()
        except PreenchaTudo:
            self.mensagem('Erro', 'Preencha todos os campos!')
        except FaltouCode:
            self.mensagem('Erro', 'Informe um código!')
        except FaltouAno:
            self.mensagem('Erro', 'Informe um ano!')
        except AnoInvalido:
            self.mensagem('Erro', 'Ano inválido!')
            self.limiteIns.inputAno.delete(0, len(self.limiteIns.inputAno.get()))
        except VeioDoPassado:
            self.mensagem('Erro', 'Por que cadastrar uma grade do passado?')
            self.limiteIns.inputAno.delete(0, len(self.limiteIns.inputAno.get()))
        except FaltouSemestre:
            self.mensagem('Erro', 'Informe um semestre!')
        except SemestreComLetra:
            self.mensagem('Erro', 'O número do semestre não pode ser uma letra!')
        # except SemestreInvalido:
        #     self.mensagem('Erro', 'Semestre inválido! Lembre-se: um ano só possui dois semestres.')
        except CodeInvalido:
            self.mensagem('Erro', """Seu código deve conter no máximo 5 caracteres e não pode conter espaços!
        Exemplos: 'SIN', 'CC01', '12345', 'ECO15' ...""")
            self.limiteIns.inputCode.delete(0, len(self.limiteIns.inputCode.get()))
        
        else:
            code = self.limiteIns.inputCode.get()
            ano = self.limiteIns.inputAno.get()
            semest = self.limiteIns.escolhaSemest.get()
            grade = Grade(code, ano, semest)            
            try:
                for grad in self.listaGrades:
                        if grade.getCodigo() == grad.getCodigo() and grade.getAno() == grad.getAno() and grade.getSemestre() == grad.getSemestre():
                            raise GradeDuplicada()
            except GradeDuplicada:
                self.mensagem('Operação não permitida', 'Esta grade já foi cadastrada!')

            else:        
                self.limiteInsDisc = LimiteInsereDiscNaGrade(self, grade)

    def insereDisciplina(self, event):
        try:
            if len(self.limiteInsDisc.escolhaDisc.get()) == 0:
                  raise FaltouDisc()
            if len(self.limiteInsDisc.escolhaPeriodo.get()) == 0:
                raise FaltouPeriodo()
            if self.isNumber(self.limiteInsDisc.escolhaPeriodo.get()) == False or int(self.limiteInsDisc.escolhaPeriodo.get()) < 1 or int(self.limiteInsDisc.escolhaPeriodo.get()) > 10:
                raise PeriodoInvalido()
        except FaltouDisc:
            self.mensagem('Erro', 'Informe uma disciplina!')
        except FaltouPeriodo:
            self.mensagem('Erro', 'Informe um período!')
        except PeriodoInvalido:
            self.mensagem('Erro', 'Período inválido!')

        else:
            periodo = int(self.limiteInsDisc.escolhaPeriodo.get())
            discipSel = self.limiteInsDisc.escolhaDisc.get()
            disciplina = self.CtrlPrincipal.ctrlDisciplina.getDisciplina(discipSel)
            disciplinaGrade = DisciplinaGrade(periodo, disciplina)
            grade = self.limiteInsDisc.retornaGrade()
            try:
                if len(grade.getDisciplina()) != 0:
                    for discGrade in grade.getDisciplina():
                        if disciplinaGrade.getDisciplinaGrade().getCodigo() == discGrade.getDisciplinaGrade().getCodigo() and disciplinaGrade.getPeriodo() == discGrade.getPeriodo():
                            raise DiscJaCadastrada()
                        if disciplinaGrade.getDisciplinaGrade().getCodigo() == discGrade.getDisciplinaGrade().getCodigo() and disciplinaGrade.getPeriodo() != discGrade.getPeriodo():
                            raise DiscCadastradaAPeriodoAnterior()
            except DiscJaCadastrada:
                self.mensagem('Erro', 'Esta disciplina já foi cadastrada!')
            except DiscCadastradaAPeriodoAnterior:
                self.mensagem('Erro', 'Esta disciplina já foi cadastrada nessa mesma grade em um período anterior!')
            else:
                grade.addDisciplina(disciplinaGrade)
                self.mensagem('Sucesso', 'Disciplina adicionada!') 
    
    def mostraGrades(self):
        if len(self.listaGrades) != 0 and self.CtrlPrincipal.ctrlCurso.retornaTamanhoListaCursos() == 0:
            self.mensagem('Erro', 'Não há cursos cadastrados para mostrar sua respectiva grade.') 
        if len(self.listaGrades) == 0:
            self.mensagem('Erro', 'Não há grades cadastradas')     
        if len(self.listaGrades) != 0 and self.CtrlPrincipal.ctrlCurso.retornaTamanhoListaCursos() != 0:
            self.limiteMost = LimiteMostraGrades(self)
    
    def BuscarGradeHandler(self, event):
        try:
            if len(self.limiteMost.inputNomeOuCode.get()) == 0:
                raise PreenchaTudo()
        except PreenchaTudo:
            self.mensagem('Erro', 'Digite o código ou o nome de um curso!')

        else:  
            grade = self.getGradePorCurso(self.limiteMost.inputNomeOuCode.get())
            self.limiteShowDis = LimiteShowDiscGrade(self, grade)
            self.limiteMost.destroy()

    def SaiInsGradHandler(self, event):
        self.limiteIns.destroy()
    
    def SaiMostGradHandler(self, event):
        self.limiteMost.destroy()
    
    def SaiShowDiscHandler(self, event):
        self.limiteShowDis.destroy()
    
    def CriaDefinitivo(self, event):
        grade = self.limiteInsDisc.retornaGrade()
        self.listaGrades.append(grade)
        self.limiteInsDisc.destroy()
        self.limiteIns.destroy()
        self.mensagem('Inserção realizada', 'Grade criada com sucesso!')
    
    def MostrarDiscHandler(self, event):
        grade = self.limiteShowDis.retornaGrad()
        periodo = self.limiteShowDis.escolhaPeriod.get()
        self.show(grade, periodo)

    def show(self, grade, periodo):
        self.__grade = grade
        self.__periodo = periodo
        try:
            if int(self.__periodo) > 10 or int(self.__periodo) < 1:
                raise GradeDontHaveThisPeriod()
        except GradeDontHaveThisPeriod:
            titulo = 'Tem algo errado'
            str = 'Esta grade não tem este período, nem disciplinas cadastradas para o mesmo!'
        else: 
            str = ''  
            titulo = ('Disciplinas da grade no período {}'.format(self.__periodo))         
            for discGrade in self.__grade.getDisciplina():
                if int(discGrade.getPeriodo()) == int(self.__periodo):
                    str += '_________________________________________________________\n'
                    str += discGrade.getDisciplinaGrade().getCodigo() + ' - ' + discGrade.getDisciplinaGrade().getNome() + '\n'
                    str += 'Carga horária: ' + discGrade.getDisciplinaGrade().getCargaHoraria() + '\n'
                    str += '_________________________________________________________\n'

        self.mensagem(titulo, str)