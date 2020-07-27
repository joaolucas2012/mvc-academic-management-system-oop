import tkinter as tk
import disciplina as disc
import grade as grd
import curso as crs
import aluno as alu
import historico as hist

class LimitePrincipal():
    def __init__(self, raiz, controle):
        self.controle = controle
        self.raiz = raiz
        self.raiz.geometry("300x250")
        self.menubar = tk.Menu(self.raiz)
        self.disciplinaMenu = tk.Menu(self.menubar)
        self.gradeMenu = tk.Menu(self.menubar)
        self.cursoMenu = tk.Menu(self.menubar)
        self.alunoMenu = tk.Menu(self.menubar)
        self.historicoMenu = tk.Menu(self.menubar)
        self.sairMenu = tk.Menu(self.menubar)

        self.disciplinaMenu.add_command(label = "Insere", command = self.controle.insereDisciplina)
        self.disciplinaMenu.add_command(label = "Mostra", command = self.controle.mostraDisciplinas)
        self.menubar.add_cascade(label = "Disciplina", menu = self.disciplinaMenu)

        self.gradeMenu.add_command(label = "Insere", command = self.controle.insereGrade)
        self.gradeMenu.add_command(label = "Mostra", command = self.controle.mostraGrades)
        self.menubar.add_cascade(label = "Grade", menu = self.gradeMenu)

        self.cursoMenu.add_command(label = "Insere", command = self.controle.insereCurso)
        self.cursoMenu.add_command(label = "Mostra", command = self.controle.mostraCursos)
        self.menubar.add_cascade(label = "Curso", menu = self.cursoMenu)

        self.alunoMenu.add_command(label = "Insere", command = self.controle.insereAluno)
        self.alunoMenu.add_command(label = "Mostra", command = self.controle.mostraAlunos)
        self.menubar.add_cascade(label = "Aluno", menu = self.alunoMenu)

        self.historicoMenu.add_command(label = "Insere", command = self.controle.insereHistoricos)
        self.historicoMenu.add_command(label = "Mostra", command = self.controle.mostraHistoricos)
        self.menubar.add_cascade(label = "Histórico", menu = self.historicoMenu)

        self.sairMenu.add_command(label="Salva", command=self.controle.salvaDados)
        self.menubar.add_cascade(label="Sair", menu=self.sairMenu)

        self.raiz.config(menu = self.menubar)

class ControlePrincipal():       
    def __init__(self):
        self.raiz = tk.Tk()
        
        self.ctrlDisciplina = disc.CtrlDisciplina()
        self.ctrlGrade = grd.CtrlGrade(self)
        self.ctrlCurso = crs.CtrlCurso(self)
        self.ctrlAluno = alu.CtrlAluno(self)
        self.ctrlHistorico = hist.CtrlHistorico(self)
        
        self.limite = LimitePrincipal(self.raiz, self)

        self.raiz.title("Sistema de Gestão Acadêmico")
        self.raiz.geometry('500x200')

        self.frameBemVindo = tk.Frame(self.raiz)
        self.frameBemVindo.pack()
        str =  "\nBem vindo!\n"
        str += "1 - Comece inserindo disciplinas\n"
        str += '2 - Insira uma grade\n'
        str += '3 - Insira um curso\n'
        str += '4 - Insira um aluno\n'
        str += '5 - Insira um histórico de disciplinas cursadas a este aluno!\n'
        str += "6 - Você pode consultar tudo o que foi cadastrado clicando em 'mostrar'\n "
        str += "7 - Para salvar as inserções, clique em Sair -> Salvar \n"
        str += '8 - Pronto!'
        self.labelEnunciado = tk.Label(self.frameBemVindo, text = str, font = ('Negrito', 9))
        self.labelEnunciado.pack(side = 'left')

        self.raiz.mainloop()
    
    def insereDisciplina(self):
        self.ctrlDisciplina.insereDisciplina()

    def mostraDisciplinas(self):
        self.ctrlDisciplina.mostraDisciplinas() 
    
    def insereGrade(self):
        self.ctrlGrade.insereGrade()

    def mostraGrades(self):
        self.ctrlGrade.mostraGrades()
    
    def insereCurso(self):
        self.ctrlCurso.insereCurso()

    def mostraCursos(self):
        self.ctrlCurso.mostraCursos()

    def insereAluno(self):
        self.ctrlAluno.insereAluno()

    def mostraAlunos(self):
        self.ctrlAluno.mostraAlunos()

    def insereHistoricos(self):
        self.ctrlHistorico.insereHistorico()

    def mostraHistoricos(self):
        self.ctrlHistorico.mostraHistoricos() 

    def salvaDados(self):
        self.ctrlDisciplina.salvaDisciplinas()
        self.ctrlGrade.salvaGrades()
        self.ctrlCurso.salvaCursos()
        self.ctrlAluno.salvaAlunos()
        self.raiz.destroy()

if __name__ == '__main__':
    c = ControlePrincipal()