import pygame, operator, math, ButtonsInfoModule, threading
from sys import exit

pygame.init()

# GUI VARIABLES / SETUP #

ScreenSizeX, ScreenSizeY = 400, 600
Screen = pygame.display.set_mode((ScreenSizeX, ScreenSizeY))
pygame.display.set_caption("Calc")

BigFont = pygame.font.Font("Assets/FiraMath-Regular.otf", 40)
Font = pygame.font.Font("Assets/FiraMath-Regular.otf", 30)
SmallFont = pygame.font.Font("Assets/FiraMath-Regular.otf", 20)
SuperSmallFont = pygame.font.Font("Assets/FiraMath-Regular.otf", 15)

# SFX #

EnterSound = pygame.mixer.Sound("Assets/ButtonSoundEffect.mp3")

# IMPORTANT VARIABLES #

clock = pygame.time.Clock()

IsThreading = False

FullAnswerText = None
CurrentAnswerText = "0"
FullEquation = "0"

MaxDigits = 15
MaxValue = ""

for I in range(MaxDigits):
    MaxValue += "9"

AwaitingNumber = False # Custom rooting / power
AwaitingNumberOperation = None
PreAwaitingNumber = None

NumberOne = None
Operation = None
NumberTwo = None

LeftClickable = False
LineShowing = False

# CLASS GROUPS #

ButtonGroup = pygame.sprite.Group()

# CLASSES #

class Button(pygame.sprite.Sprite):
    def __init__(self, ButtonName, ButtonInfo):
        super().__init__()

        ButtonGroup.add(self)

        self.Name = ButtonName
        self.Rect = pygame.Rect((0, 0), ButtonInfo["Size"])
        self.Rect.center = (ButtonInfo["Position"][0] - 4, ButtonInfo["Position"][1])

        if CheckIfButtonNameIsNumber(ButtonName): 
            self.DefaultColor = (87, 87, 87)
            self.HoveredColor = (150, 150, 150)
            self.TextColor = "WHITE"
        elif ButtonName == "AC" or ButtonName == "DEL":
            self.DefaultColor = (150, 150, 150)
            self.HoveredColor = (255, 255, 255)
            self.TextColor = "BLACK"
        else:
            self.DefaultColor = (130, 61, 0)
            self.HoveredColor = "ORANGE"
            self.TextColor = "WHITE"

        self.TextLabel = Font.render(ButtonName, False, self.TextColor)
        self.TextLabelRect = self.TextLabel.get_rect()
        self.TextLabelRect.center = self.Rect.center

    def CheckIfPlayerClicked(self):
        if self.Rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(Screen, self.HoveredColor, self.Rect, 0, 50)

            if pygame.mouse.get_pressed()[0] and LeftClickable:
               InsertStringToText(self.Name)

    def update(self):
        pygame.draw.rect(Screen, self.DefaultColor, self.Rect, 0, 50)

        self.CheckIfPlayerClicked()
        
        Screen.blit(self.TextLabel, self.TextLabelRect)

# FUNCTIONS #

def CheckIfButtonNameIsNumber(ButtonName):
    try:
        float(ButtonName)
        return True
    except ValueError:
        return False

def ResetVariables():
    global NumberOne, NumberTwo, Operation, AwaitingNumber, FullAnswerText

    NumberOne = None
    NumberTwo = None
    Operation = None
    AwaitingNumber = False
    FullAnswerText = None

def CheckIfOperator(StringValue : str):
    return StringValue == "+" or StringValue == "-" or StringValue == "×" or StringValue == "÷"

def Calculate():
    if Operation == "÷" and NumberTwo == "0": return "0"

    Answer = ButtonsInfoModule.OperationsTable[Operation](float(FullAnswerText if FullAnswerText else NumberOne), float(NumberTwo))
    if Answer % 1 == 0: Answer = int(Answer) # Turn into whole number if no decimals
    return str(Answer)

def CustomCalculate():
    if AwaitingNumberOperation == "Root" and CurrentAnswerText == "0": return

    if AwaitingNumberOperation == "Root":
        Answer = float(PreAwaitingNumber)**(1/float(CurrentAnswerText))
    elif AwaitingNumberOperation == "Exponent":
        Answer = float(PreAwaitingNumber)**float(CurrentAnswerText)

    if Answer % 1 == 0: Answer = int(Answer) # Turn into whole number if no decimals

    if math.isclose(Answer, round(Answer)): # Rounding lol
        Answer = round(Answer)

    return str(Answer)

def CompactNumber():
    NumberLength = len(FullAnswerText)
    ToDivideNumber = 1

    for i in range(NumberLength - 1):
        ToDivideNumber *= 10

    FirstString = (float(FullAnswerText) / ToDivideNumber)

    if FirstString != math.inf and FirstString != -math.inf and math.isclose(FirstString, round(FirstString)): # Rounding lol
        FirstString = round(FirstString)

        if FirstString == 10: # For some reason if you spam 10x10 python does this weird glitch where the number is offset by like 1 decimal
            FirstString = 1
            NumberLength += 1

    BackText = "×10^" + str(NumberLength - 1)

    return str(FirstString)[:MaxDigits - len(BackText)] + BackText

def UpdateCalculation(Answer):
    global FullAnswerText

    if "e" in Answer: ResetVariables(); CurrentAnswerText = "0"; return "Error" # When number too big or too small

    if abs(float(Answer)) > (float(MaxValue)):
        FullAnswerText = Answer
        Answer = CompactNumber()

    if len(Answer) > MaxDigits - 1: Answer = Answer[:MaxDigits] # Cant make text too long

    return Answer

def ErrorMsgDisplay(Message : str):
    global FullEquation, IsThreading

    IsThreading = True

    PreviousFullEquationText = FullEquation if FullEquation else ""

    FullEquation = Message

    def RevertText():
        global FullEquation, IsThreading

        FullEquation = PreviousFullEquationText
        IsThreading = False

    threading.Timer(1.0, RevertText).start()

def InsertStringToText(StringValue : str):
    if IsThreading: return

    global CurrentAnswerText, NumberOne, NumberTwo, Operation, AwaitingNumber, PreAwaitingNumber, AwaitingNumberOperation, FullAnswerText

    if CheckIfOperator(StringValue): # OPERATORS
        if CheckIfOperator(CurrentAnswerText): CurrentAnswerText = StringValue; return # If operator already chosen in answer box

        if NumberOne and Operation and not "Ans" in FullEquation:
            NumberTwo = CurrentAnswerText
            NumberOne = Calculate()
        else:
            NumberOne = CurrentAnswerText
            
        Operation = None
        NumberTwo = None
        CurrentAnswerText = StringValue
    else: # EVERYTHING ELSE
        if StringValue == "AC": # Clear Button
            CurrentAnswerText = "0"
            ResetVariables()
            return

        if StringValue == "DEL": # Delete Button
            if CheckIfOperator(CurrentAnswerText): return

            if FullAnswerText and not AwaitingNumber:
                FullAnswerText = FullAnswerText[:-1]

                if abs(float(FullAnswerText)) > (float(MaxValue)):
                    CurrentAnswerText = CompactNumber()
                else:
                    CurrentAnswerText = FullAnswerText
                    FullAnswerText = None
                
                return

            if len(CurrentAnswerText) == 1:
                CurrentAnswerText = "0"
            else:
                CurrentAnswerText = CurrentAnswerText[:-1]
                if CurrentAnswerText == "-": CurrentAnswerText = "0"

            if NumberTwo: NumberOne = CurrentAnswerText
            return
        
        if StringValue == "+/-": # Change from position to negative and vice versa
            if not CheckIfOperator(CurrentAnswerText):
                if FullAnswerText:
                    ErrorMsgDisplay("Clear Compacted Number First")
                    return
                else:
                    Answer = -float(CurrentAnswerText)
                    if Answer % 1 == 0: Answer = int(Answer)
                    CurrentAnswerText = str(Answer)

                return
            
        if StringValue == "√": # Square root
            if FullAnswerText:
                if float(FullAnswerText) < 0:
                    ErrorMsgDisplay("You Can't Root a Negative")
                    return

                if CheckIfOperator(StringValue): return
                Answer = str(math.sqrt(float(FullAnswerText)))
            else:
                if float(CurrentAnswerText) < 0:
                    ErrorMsgDisplay("You can't root a negative")
                    return

                if CheckIfOperator(StringValue): return
                Answer = str(math.sqrt(float(CurrentAnswerText)))

            if float(Answer) % 1 == 0: Answer = int(float(Answer)) # Turn into whole number if no decimals

            CurrentAnswerText = CurrentAnswerText = UpdateCalculation(str(Answer))

            if NumberTwo: NumberOne = CurrentAnswerText

        if StringValue == "n√": # Custom root
            if FullAnswerText:
                if float(FullAnswerText) < 0:
                    ErrorMsgDisplay("You can't root a negative")
                    return

                if CheckIfOperator(StringValue): return
                Answer = str(math.sqrt(float(FullAnswerText)))
            else:
                if float(CurrentAnswerText) < 0:
                    ErrorMsgDisplay("You can't root a negative")
                    return

            if AwaitingNumber:
                AwaitingNumber = False
                return
            else:
                AwaitingNumber = True
                PreAwaitingNumber = FullAnswerText if FullAnswerText else CurrentAnswerText
                CurrentAnswerText = "0"
                AwaitingNumberOperation = "Root"

        if StringValue == "x²": # Square
            if CheckIfOperator(StringValue): return

            try:
                Answer = (float(FullAnswerText if FullAnswerText else CurrentAnswerText)**2)
            except:
                ErrorMsgDisplay("Answer is too large"); return
            
            if float(Answer) % 1 == 0: Answer = int(float(Answer)) # Turn into whole number if no decimals

            CurrentAnswerText = CurrentAnswerText = UpdateCalculation(str(Answer))
            if CurrentAnswerText == "Error": CurrentAnswerText = "0"; return

            if NumberTwo: NumberOne = CurrentAnswerText

        if StringValue == "x^y": # Custom exponent
            if CheckIfOperator(CurrentAnswerText): return

            if AwaitingNumber:
                AwaitingNumber = False
                return
            else:
                AwaitingNumber = True
                PreAwaitingNumber = FullAnswerText if FullAnswerText else CurrentAnswerText
                CurrentAnswerText = "0"
                AwaitingNumberOperation = "Exponent"

        if StringValue == "." and CurrentAnswerText.find(".") >= 1: return # No more than one decimal

        if StringValue == "=": # Calculate
            if AwaitingNumber: # Custom root / exponent
                if CheckIfOperator(CurrentAnswerText): return
                if AwaitingNumberOperation == "Root" and CurrentAnswerText == "0": ErrorMsgDisplay("You can't root by zero"); return

                if AwaitingNumberOperation == "Exponent":
                    try: 
                        abs(float(PreAwaitingNumber))**float(CurrentAnswerText)
                    except:
                        ErrorMsgDisplay("Answer is too large"); return

                EnterSound.play()

                Answer = CustomCalculate()
                CurrentAnswerText = UpdateCalculation(Answer)

                if abs(float(Answer)) <= (float(MaxValue)): FullAnswerText = ""

                AwaitingNumber = False
                return

            if NumberOne and Operation:
                EnterSound.play()
                if not NumberTwo: NumberTwo = CurrentAnswerText
                
                Answer = Calculate()
                CurrentAnswerText = UpdateCalculation(Answer)
                if CurrentAnswerText == "Error": CurrentAnswerText = "0"; return
                NumberOne = CurrentAnswerText
                return
            else: return
        
        if len(CurrentAnswerText) > MaxDigits - 1: return # Cant make text too long

        if StringValue == "=" or StringValue == "+/-" or StringValue == "√" or StringValue == "x²" or StringValue == "x^y" or StringValue == "n√": return # Banned letters from appearing on screen

        if CheckIfOperator(CurrentAnswerText) and StringValue != "=": # Assign Operator
            Operation = CurrentAnswerText
            CurrentAnswerText = "" 
        
        if CurrentAnswerText == "0":
            if StringValue == ".": CurrentAnswerText = "0."; return

            CurrentAnswerText = StringValue
        else:
            if CurrentAnswerText == "" and StringValue == ".": CurrentAnswerText = "0" # For pressing . after operator

            if NumberTwo and not AwaitingNumber:
                ResetVariables()
                CurrentAnswerText = ""

            CurrentAnswerText += StringValue

def CreateAnswerBox():
    global FullEquation

    AnswerText = BigFont.render(CurrentAnswerText, False, "WHITE")
    AnswerTextRect = AnswerText.get_rect()
    AnswerTextRect.bottomright = (ScreenSizeX - 35, 90 + AnswerTextRect.height - 4)
    Screen.blit(AnswerText, AnswerTextRect)

    if not IsThreading:
        if NumberOne and NumberTwo and Operation: # If theres already a complete equation (after pressing =)
            FullEquation = "(Ans)" + Operation + NumberTwo
        else:
            FullEquation = (NumberOne if NumberOne else "") + (Operation if Operation else "") + (NumberTwo if NumberTwo else "") + CurrentAnswerText

        if AwaitingNumber: FullEquation = "Insert Index / Exponent value"

    FullEquationText = SmallFont.render(FullEquation, False, "GRAY")
    FullEquationTextRect = FullEquationText.get_rect()
    FullEquationTextRect.bottomright = (ScreenSizeX - 35, 90 + FullEquationTextRect.height - 30)
    Screen.blit(FullEquationText, FullEquationTextRect)

def Credit():
    CreditText = SuperSmallFont.render("Calc by Lin. Ver. 1.0.0", False, "WHITE")
    CreditTextRect = CreditText.get_rect()
    CreditTextRect.center = (ScreenSizeX / 2, ScreenSizeY - 40)
    Screen.blit(CreditText, CreditTextRect)

def CreateLine():
    global LineShowing

    if LineShowing:
        LineRect = pygame.Rect((0, 0, 2, 40))
        LineRect.center = (ScreenSizeX - 32, 104)
        pygame.draw.rect(Screen, "WHITE", LineRect)

def SetUpUIS():
    CreateAnswerBox()
    CreateLine()
    Credit()

# SET UP #

for ButtonLetter, ButtonInfo in ButtonsInfoModule.ButtonsInfoTable.items(): Button(f"{ButtonLetter}", ButtonInfo) # Make all the buttons

# TIMERS #

DisplayLine = pygame.USEREVENT + 1
pygame.time.set_timer(DisplayLine, 500)

# THE PROGRAM LOOP #

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == DisplayLine:
            LineShowing = not LineShowing
        if event.type == pygame.KEYDOWN:
            if event.unicode.isdigit():
                InsertStringToText(str(event.unicode))
            if event.key == pygame.K_RETURN or event.unicode == "=": # Equals
                InsertStringToText("=")
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE: # Delete
                InsertStringToText("DEL")
            if event.unicode == "+" or event.unicode == "-" or event.unicode == "/" or event.unicode == "x":
                InsertStringToText(ButtonsInfoModule.KeyboardValues[event.unicode])

    Screen.fill("BLACK")
    SetUpUIS()

    ButtonGroup.update()

    LeftClickable = not pygame.mouse.get_pressed()[0] # Click debounce
    pygame.display.update()
