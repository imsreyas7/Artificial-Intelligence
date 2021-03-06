class DPLL:
    true_literals = set()
    false_literals = set()
    pure_literals = set()
    cnf = []
    literals = []
    unit_props, num_pure, branches = 0, 0, 0
    
    def __init__(self, formula):
        """To initialize the DPLL Solver with the required CNF Form & Literals. """
        
        self.literals = [literal for literal in list(set(formula)) if literal.isalpha()]
        self.cnf = formula.split(", ")
        self.pure_literals = set()

        print("Initial Formula:\t\t\t", self)
        
        
    def __str__(self):
        """To convert the Pythonic-list used for CNF notation into a readable formula in CNF. """
        
        cnf_str = ""
        
        for clause in self.cnf:  #represent each claue in CNF
            if len(clause) > 0:
                cnf_str += '(' + clause.replace(' ', ' ∨ ') + ') ∧ '
    
        if cnf_str == "":       #formula is empty
            cnf_str = "()"
            
        if cnf_str[-2] == "∧":  #removing the final '∧' added which is un-wanted.
            cnf_str = cnf_str[:-2:] 
    
        return cnf_str

    
    def find_literals(self, formula):
        """Finds the literals existing in a given formula. """

        literals = [literal for literal in list(set(''.join(formula))) if literal.isalpha()]

        return literals
    
    def remove_pure_literals(self):
        """Finds the pure literals in the given formula. """

        cnf = list(set(self.cnf))
        unit_clauses = [clause for clause in cnf if len(clause) < 3]
        unit_clauses = list(set(unit_clauses))
        current_literals = self.find_literals(cnf)  #Find literals in the current formula

        for literal in current_literals:  #Check for literals like X
            is_pure_literal = False

            for i in range(len(cnf)):
                if '¬' + literal not in cnf[i]: 
                    is_pure_literal = True
                else:  #If ¬X exists in other clauses
                    is_pure_literal = False
                    break
            
            if is_pure_literal:  #If X is a pure literal
                self.num_pure += 1
                self.pure_literals.add(literal)
                self.true_literals.add(literal)  #Add X to True literals
                i = 0

                while True:  #Remove clauses containing X
                    if i >= len(cnf):
                        break

                    if literal in cnf[i]:
                        cnf.remove(cnf[i])
                    
                        i -= 1
                    i += 1

        for literal in current_literals:  #Check for literals like ¬X 
            literal = '¬' + literal  #Search for literals of the type ¬X
            is_pure_literal = False

            for i in range(len(cnf)):
                if literal in cnf[i]: 
                    is_pure_literal = True
                else:  #If X exists in other clauses
                    is_pure_literal = False
                    break
            
            if is_pure_literal:  #If ¬X is a pure literal
                self.num_pure += 1
                self.pure_literals.add(literal)
                self.false_literals.add(literal[-1])  #Add X to False literals
                i = 0

                while True:  #Remove clauses containing ¬X
                    if i >= len(cnf):
                        break

                    if literal in cnf[i]:
                        cnf.remove(cnf[i])
                    
                        i -= 1
                    i += 1
        
        self.cnf = cnf

        print("Pure Literals:\t\t\t\t", list(self.pure_literals))
        print("CNF after removing Pure Literals:\t", self)

        return cnf

    
    def unit_clause_propagation(self):
        """Peform the unit-clause propagation on the given formula. """
        
        new_true_literals  =  []
        new_false_literals =  []
        
        print("\nCurrent Formula:\t\t\t", self)
        
        cnf = list(set(self.cnf))
        unit_clauses = [clause for clause in cnf if len(clause) < 3]   #clause of len < 3 is a unit clause
        unit_clauses = list(set(unit_clauses))
        
        if unit_clauses:  #Assign truth values to unit clauses for satisfying the given formula
            for unit in unit_clauses:
                self.unit_props += 1
                
                if '¬' in unit:  #False unit clause
                    self.false_literals.add(unit[-1])
                    new_false_literals.append(unit[-1])
                    i = 0
                    
                    while True:
                        if unit in cnf[i]:  #Remove the unit clause from the formula
                            cnf.remove(cnf[i])
                            i -= 1
                        
                        elif unit[-1] in cnf[i]:  #If a ¬(unit clause) exists in the formula
                            cnf[i] = cnf[i].replace(unit[-1], '').strip()
                    
                        i += 1
                    
                        if i >= len(cnf):
                            break
        
                else:  #True unit clause
                    self.true_literals.add(unit)
                    new_true_literals.append(unit)
                    i = 0
                
                    while True:
                        if '¬' + unit in cnf[i]:  #If a ¬(unit clause) exists in the formula
                            cnf[i] = cnf[i].replace('¬' + unit, '').strip()
                        
                            if '  ' in cnf[i]:  #Empty clause
                                cnf[i] = cnf[i].replace('  ', ' ')
                        
                        elif unit in cnf[i]:  #Remove the unit clause from the formula
                            cnf.remove(cnf[i])
                            i -= 1
                            
                        i += 1
                        
                        if i >= len(cnf):
                            break
        
        self.cnf = cnf

        print("Current Unit Clauses:\t\t\t", unit_clauses)
        print("CNF after doing Unit Propagation:\t", self)

        return cnf, new_true_literals, new_false_literals
    
    
    def DPLL_Algorithm(self):
        """Perform the David-Putnam-Logemann-Loveland algorithm on the given formula. """
        
        self.true_literals = set(self.true_literals)
        self.false_literals = set(self.false_literals)
        
        self.branches += 1  #Since this is a new branch

        self.cnf, new_true_literals, new_false_literals = self.unit_clause_propagation()  #Do unit-clause propagation

        if sum(len(clause) == 0 for clause in self.cnf):  #If there are empty parantheses, indicating contradiction
            
            for literal in new_true_literals:   #clear every newly set true literal
                self.true_literals.remove(literal)
            
            for literal in new_false_literals:  #clear every newly set false literal
                self.false_literals.remove(literal)
                
            print("\nNull clause found. Backtracking...")
            
            return False  #Backtrack, since we cannot simplify anymore, and it is unsatisfiable in the current branch


        self.cnf = self.remove_pure_literals()  #Removing pure literal containing clauses from the formula

        cnf = self.cnf

        if len(self.cnf) == 0:  #No more clauses to satisfy
            return True

        
        self.literals = [literal for literal in list(set(''.join(self.cnf))) if literal.isalpha()]
        #form the literals again from the updated formula
        
        first_literal = self.literals[0]  #choose the first literal to set as True/False to find satisfying assignments
        
        self.cnf = cnf + [first_literal]  #Try with first literal set to True
        print("\nTrying with {0} as True...".format(first_literal))
        
        if self.DPLL_Algorithm():  #recursively work on the new formula
            return True
        
        self.cnf = cnf + ['¬' + first_literal]  #Try with first literal set to False (i.e ¬(first literal) is True)
        print("\nTrying with ¬{0} as True...".format(first_literal))
        
        if self.DPLL_Algorithm():  #recursively work on the new formula
            return True

        
        else:  #no satisfying assignments were found to the literals of the formula
            self.cnf = cnf
            
            for literal in new_true_literals:   #remove all the assignments
                self.true_literals.remove(literal)
            
            for literal in new_false_literals:  #remove all the assignments
                self.false_literals.remove(literal)
            
            return False  #the formula is unsatisfiable.
        
    
    def print_result(self, satisfiability):
        """Print the result of the DPLL Algorithm on the formula along with its literals' assignments and statistics. """
        
        if satisfiability == True:
            print("\nThe given CNF statement is satisfiable.")
            print("\nSolution: ")
            
            for literal in self.true_literals:
                print("\t"+literal, "= True")
                
            for literal in self.false_literals:
                print("\t"+literal, "= False")
            
        else:
            print("\nThe given CNF statement was unsatisfiable.")
            
        print("\nNo. of branches:\t\t", self.branches)
        print("\nNo. of unit propagations:\t", self.unit_props)
        print("\nNo. of pure literals removed:\t", self.num_pure)

# Running DPLL Algorithm for  (X∨Y∨Z)∧(X∨¬Y∨Z)∧(¬X∨Y∨¬Z)∧(¬Z)

dpll_solver = DPLL("¬X Y Z, ¬X ¬Y Z, ¬X Y ¬Z, ¬Z")
satisfiability = dpll_solver.DPLL_Algorithm()
dpll_solver.print_result(satisfiability)

# Running DPLL Algorithm for  (¬P∨Q)∧(¬Q∨¬R)∧(¬S∨P)∧(P∨Q∨¬R)

dpll_solver = DPLL("¬P Q, ¬Q ¬R, R ¬S, ¬S P, P Q ¬R")
satisfiability = dpll_solver.DPLL_Algorithm()
dpll_solver.print_result(satisfiability)

# Custom formula : Separate clauses in formula by commas ", " and literals inside a clause with spaces. Use "¬" for negation of a literal.

dpll_solver = DPLL(input("Enter a formula in CNF: "))
satisfiability = dpll_solver.DPLL_Algorithm()
dpll_solver.print_result(satisfiability)

# (X ∨ Y) ∧ (Y ∨ ¬X) ∧ (¬X ∨ ¬Y) 
dpll_solver = DPLL("X Y, Y ¬X, ¬X ¬Y")
satisfiability = dpll_solver.DPLL_Algorithm()
dpll_solver.print_result(satisfiability)