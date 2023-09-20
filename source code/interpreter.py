from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.simpledialog import askstring
import tkinter.scrolledtext as scrolledtext
import re

# Global Variables
index = 0
get_var = ""
var_ident = ""
smoosh_str = ""
print_bool = False
var_decl_bool = False
assignment_bool = False
arity_bool = False
eval_bool = True
break_bool = False
switch_eval_bool = False
if_bool = True
loop_bool = False
loop_eval = False
loop_start = 0
loop_end = 0
print_stack = []
expression_stack = []
arity_stack = []
if_else_block = []
switch_block = []
switch_or_if_else_block = []
oic_line_num = []
omg_line_num = []
im_in_yr_line_num = []
im_outta_yr_line_num = []
symbols = {"IT": "NOOB"}

# For opening a file dialog
def select_file():

    # File dialog that only accepts .lol files
    file_path = fd.askopenfilename(title="Open a LOLCODE file..", filetypes=(("lol files", ".lol"),)) 

    # No file selected
    if len(file_path) == 0: return 

    # Get the file contents
    file_contents = read_file(file_path)

    # Show file contents to GUI
    show_file_contents(file_contents) 

# For opening a file
def read_file(filename):

    file = open(filename, "r")

    contents = file.read() 
	
    file.close()

    return contents

# For showing file contents to GUI
def show_file_contents(contents):

    # Make sure text editor is clear
    text_editor.delete(1.0, END)

    # Print contents to GUI
    text_editor.insert(1.0, contents)

def populate_table(table, contents):
    for row in table.get_children():
        table.delete(row)
    
    # Symbol Table
    if type(contents) is dict:
        left = list(contents.keys())
        right = list(contents.values())

        for i in range(len(contents)):
            table.insert(parent='', index=END, text=i, values=(left[i], right[i])) # print to GUI
    
    # Lexemes
    else:
        for i in range(len(contents)):
            table.insert(parent='', index=END, text=i, values=(contents[i][0], contents[i][1])) # print to GUI
        
# For printing error into GUI
def print_error(error):
    console["state"] = "normal"
    console.insert(END, error)
    console.insert(END, "\n") 
    console["state"] = "disabled"

# Run interpreter here
def run():

	# Reset variables
    global symbols, index, var_ident, print_stack, expression_stack, if_else_block, switch_block, switch_or_if_else_block, oic_line_num, arity_stack, break_bool, if_bool
    global omg_line_num, im_in_yr_line_num, im_outta_yr_line_num, smoosh_str, print_bool, var_decl_bool, assignment_bool, get_var, arity_bool, eval_bool, switch_eval_bool
    global loop_bool, loop_start, loop_end, loop_eval

    symbols = {"IT": "NOOB"}
    index = 0
    get_var = ""
    var_ident = ""
    smoosh_str = ""
    print_bool = False
    var_decl_bool = False
    assignment_bool = False
    arity_bool = False
    eval_bool = True
    break_bool = False
    switch_eval_bool = False
    if_bool = True
    loop_bool = False
    loop_eval = False
    loop_start = 0
    loop_end = 0
    print_stack = []
    expression_stack = []
    arity_stack = []
    if_else_block = []
    switch_block = []
    switch_or_if_else_block = []
    oic_line_num = []
    omg_line_num = []
    im_in_yr_line_num = []
    im_outta_yr_line_num = []
    console["state"] = "normal"
    console.delete(1.0, END)
    console["state"] = "disabled"

    # Get input from Text widget
    temp_code = text_editor.get(1.0,'end-1c') 

    # No input
    if temp_code.strip()=='': return 

    code = read_code(temp_code)

    lexer = create_tokens(code)

    tokens = lexer[0]
    orig_tokens = lexer[1]

    populate_table(lexer_table, tokens)

    parser(tokens, orig_tokens, index)

######################### L E X I C A L  A N A L Y Z E R #########################

# Keywords dictionary
keywords = {
    "HAI" : "Code Delimiter"
    , "KTHXBYE" : "Code Delimiter"
    , "BTW" : "Single Line Comment Declaration"
    , "OBTW" : "Multi-Line Comment Delimiter"
    , "TLDR" : "Multi-Line Comment Delimiter"
    , "I HAS A" : "Variable Declaration"
    , "ITZ" : "Variable Assignment"
    , "R" : "Assignment Operator"
    , "SUM OF" : "Arithmetic Operator"
    , "DIFF OF" : "Arithmetic Operator"
    , "PRODUKT OF" : "Arithmetic Operator"
    , "QUOSHUNT OF" : "Arithmetic Operator"
    , "MOD OF" : "Arithmetic Operator"
    , "BIGGR OF" : "Arithmetic Operator"
    , "SMALLR OF" : "Arithmetic Operator"
    , "BOTH OF" : "Boolean Operator"
    , "EITHER OF" : "Boolean Operator"
    , "WON OF" : "Boolean Operator"
    , "NOT" : "Boolean Operator"
    , "ANY OF" : "Infinite Arity Operator"
    , "ALL OF" : "Infinite Arity Operator"
    , "MKAY" : "Infinite Arity Delimiter"
    , "BOTH SAEM" : "Comparison Operator"
    , "DIFFRINT" : "Comparison Operator"
    , "SMOOSH" : "Concatenation Operator"
    , "AN" : "Literal or Identifier Separator"
    , "MAEK" : "Typecast Operator"
    , "R MAEK": "Reassignment Operator"
    , "A" : "Typecast Separator"
    , "IS NOW A" : "Reassignment Operator"
    , "VISIBLE" : "Output Keyword"
    , "GIMMEH" : "Input Keyword"
    , "O RLY?" : "If Delimiter"
    , "YA RLY" : "If Keyword"
    , "MEBBE" : "Else-if Keyword"
    , "NO WAI" : "Else Keyword"
    , "OIC" : "If-Else or Switch-Case Delimiter"
    , "WTF?" : "Switch-Case Delimiter"
    , "OMG" : "Case Keyword"
    , "OMGWTF" : "Default Case Keyword"
    , "IM IN YR" : "Loop Delimiter"
    , "GTFO" : "Break Keyword"
    , "UPPIN" : "Increment Operator"
    , "NERFIN" : "Decrement Operator"
    , "YR" : "Loop Separator"
    , "TIL" : "FAIL Loop Repeater"
    , "WILE" : "WIN Loop Repeater"
    , "IM OUTTA YR" : "Loop Delimiter"
    , "HOW IZ I" : "Function Delimiter"
    , "IF U SAY SO" : "Function Delimiter"
}

# Potential keywords array
potential_keyword = ["I", "I HAS", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD"
                    , "BIGGR", "SMALLR", "BOTH", "EITHER", "WON", "ANY", "ALL"
                    , "IS", "IS NOW", "O", "YA", "NO", "IM", "IM IN", "IM OUTTA"
                    , "HOW", "HOW IZ", "IF", "IF U", "IF U SAY"
]

# Regex for identifier
identifier = "^[a-zA-Z][a-zA-Z0-9_]*$"

# Regex for NUMBR/NUMBAR (number) literals
literals = ["^-?\d+$", "^-?\d*\.\d+$"]

# Regex for YARN (string) literals
string_literal = "^\"[^”]*\"$"

# Regex for TROOF (bool) literals
bool_literal = "(WIN|FAIL)"

# Regex for TYPE literals
type_literal = "(NOOB|TROOF|NUMBAR|NUMBR|YARN)"

# For reading code
def read_code(temp_code):

    # Words array
    words = []

    for line in temp_code.split("\n"):
        line = line + "\n"
        words.append(line)
    
    # Return words array
    return words

# Create tokens here  
def create_tokens(file):
    
    # Tokens array
    tokens = []
    orig_tokens = []

    token_before = ""

    # For getting tokens
    token = ""
    orig_token = ""

    # For checking if space is encountered
    space = False
     
    # For checking if string delimiter is encountered
    string_delim = False

    # For checking if single line comment is encountered
    sline_comment = False

    # Multi-line comment boolean
    mline_comment = False

    # For taking note the line number
    line_num = 0

    # Loop through every word
    for word in file:

        # Increment line number
        line_num += 1
        
        # TLDR Keyword is encountered
        if word[len(word)-5:len(word)] == "TLDR\n":

            # Make mline_comment to False
            mline_comment = False

            # Boolean for single spacing
            temp_space = False

            # For getting the comment from token
            comment = ""

            # For char in token
            for i in token:

                # If not a trailing newline
                if i != "\n":

                    # If whitespace
                    if i == " ":

                        # If single spacing is false, add a space and make single spacing true
                        if temp_space == False:
                            comment += " "
                            temp_space = True
                    
                    # If not a whitespace, concatenate to comment and make single spacing false
                    else:
                        comment += i
                        temp_space = False

                # If trailing newline
                else:
                    # Add a whitespace if single spacing is false and make it true
                    if temp_space == False:
                        comment += " "
                        temp_space = True
            
            # Append to tokens array
            tokens.append([comment, "Multi-Line Comment", line_num-1])
            orig_tokens.append(token)

            # Make current token as previous token and reset token string
            token_before = token
            token = ""

        # Loop through every character
        for i in range(len(word)):

            # Make single line comment bool to true if token before is BTW
            if token_before == "BTW":
                sline_comment = True

            # Make multi-line comment bool to true if token before is OBTW
            if token_before == "OBTW":
                mline_comment = True

            # Make sline_comment to false if sline_comment is still true and a trailing newline is encountered
            # make space to true as well
            if sline_comment == True and word[i] == "\n":
                sline_comment = False
                space = True
                orig_token = token + "\n"

            # Append to token if mline or sline comment is true
            elif mline_comment == True or sline_comment == True:
                token += word[i]

            # Make space to true if \n, \t, or whitespace (string delimiter should be false) is encountered
            elif (word[i] == "\n")  or (word[i] == "\t") or (word[i] == " " and string_delim == False):
                space = True
                if word[i] == "\n":
                    orig_token = token + "\n"
                else:
                    orig_token = token

            # Quotation mark is encountered; toggle string_delim to its opposite boolean value
            if word[i] == "\"" and sline_comment == False or word[i] == "\"" and sline_comment == False:
                if string_delim == False:
                    string_delim = True
                else:
                    string_delim = False

            # Concatenate character to token string if character is not a space
            if space == False and mline_comment == False and sline_comment == False:
                token += word[i]
            
            # Make token if space is true
            if space == True:
                # Make space into false
                space = False

                # Token is not an empty string
                if token != "":
                    
                    # If token before is R and MAEK is the current token
                    if (token == "MAEK" and token_before == "R"):
                        # Create a temp variable and pass token to temp
                        temp = token

                        # Concatenate token before, whitespace, and temp variable to token
                        token = token_before + " " + temp

                        orig_token = token
                        # Pop the value at last index in tokens array
                        tokens.pop()
                        orig_tokens.pop()

                    # Bool for checking if token is already tokenized with a value
                    tokenized = False

                    # Check if token is in keywords dictionary
                    for key, value in keywords.items():
                        
                        # Token is found in keywords
                        if token == key:
                            
                            # Append an array of token with its value, make tokenized to true,
                            # reset value of token and break the loop of dictionary
                            tokens.append([token, value, line_num])
                            orig_tokens.append(orig_token)
                            token_before = token
                            tokenized = True
                            token = ""
                            break
                    
                    # Token not found in keywords
                    if tokenized == False:

                        # Bool for checking validity of identifier
                        append = False

                        # If potential keyword, add space
                        if token in potential_keyword:
                            token += " "
                            append = True
                            
                        else:
                            
                            # Number literal
                            for pattern in literals:

                                if re.match(pattern, token) and token_before == "HAI":
                                    tokens.append([token, "LOLCODE Version", line_num])
                                    orig_tokens.append(orig_token)
                                    append = True

                                elif re.match(pattern, token) and token_before != "BTW":
                                    int_pattern = "^-?\d+$" 
                                    flt_pattern = "^-?\d*\.\d+$"
                                    if int_pattern == pattern:
                                        token = int(token)
                                        token = str(token)
                                    elif flt_pattern == pattern:
                                        token = float(token)
                                        token = str(token)
                                    tokens.append([token, "Literal", line_num])
                                    orig_tokens.append(orig_token)
                                    append = True

                            # String literal
                            if re.match(string_literal, token):
                                
                                tokens.append([token[0], "String Delimiter", line_num])
                                tokens.append([token[1:len(token)-1], "Literal", line_num])
                                tokens.append([token[len(token)-1], "String Delimiter", line_num])

                                if orig_token[-1] != "\n":
                                    orig_tokens.append(orig_token[0])
                                    orig_tokens.append(orig_token[1:len(orig_token)-1])
                                    orig_tokens.append(orig_token[len(orig_token)-1])
                                else:
                                    orig_tokens.append(orig_token[0])
                                    orig_tokens.append(orig_token[1:len(orig_token)-2])
                                    orig_tokens.append(orig_token[len(orig_token)-2:len(orig_token)])

                                append = True

                            # Single-Line Comment
                            elif token_before == "BTW":
                                comment = ""
                                
                                for i in token:
                                    if i != "\n":
                                        comment += i       
                                
                                tokens.append([comment, "Single Line Comment", line_num])
                                orig_tokens.append(orig_token)
                                append = True

                            # Boolean literal
                            elif re.match(bool_literal, token):
                                tokens.append([token, "Boolean Literal", line_num])
                                orig_tokens.append(orig_token)
                                append = True

                            # Type literal
                            elif re.match(type_literal, token):
                                tokens.append([token, "Type Literal", line_num])
                                orig_tokens.append(orig_token)
                                append = True

                            # Identifier
                            elif re.match(identifier, token):
                                tokens.append([token, "Variable Identifier", line_num])
                                orig_tokens.append(orig_token)
                                append = True
       
                            # Print an error if invalid identifier and quit the program
                            if append == False:
                                print_error("Lexical Error! Line " + str(line_num) + ": " + str(token) + " is not valid!")
                                return
                            
                            # Record current token into token before variable
                            token_before = token

                            # Reset token
                            token = ""

    return [tokens,orig_tokens]

######################### P A R S E R #########################

# Parser starts here
def parser(tokens, orig_tokens, index):
    global oic_line_num, im_outta_yr_line_num

    for token in range(index, len(tokens)):

        # append to oic line num if OIC is found
        if tokens[token][1] == "If-Else or Switch-Case Delimiter":
            oic_line_num.append(tokens[token][2])
        
        # append to im outta yr line num if IM OUTTA YR is found
        if tokens[token][0] == "IM OUTTA YR":
            im_outta_yr_line_num.append(tokens[token][2])

    # Starts with single line comment
    if tokens[index][1] == "Single Line Comment Declaration":
        index += 1
        
        if tokens[index][1] == "Single Line Comment":

            index += 1
    
    # Starts with multi-line comment
    elif tokens[index][1] == "Multi-Line Comment Delimiter":
        index += 1
        
        if tokens[index][1] == "Multi-Line Comment":
            index += 1

            if tokens[index][1] == "Multi-Line Comment Delimiter":
                
                if orig_tokens[index] != "TLDR\n":
                    print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak expected after TLDR!")
                    return
                
                index += 1

    # HAI is found
    if tokens[index][0] == "HAI":
        # Version found
        if tokens[index+1][1] == "LOLCODE Version":
            index += 1
            if tokens[index+1][0] == "BTW" or tokens[index+1][0] == "OBTW":
                can_end = False
                
                # Start program if KTHXBYE is found
                if "KTHXBYE\n" in orig_tokens or "KTHXBYE" in orig_tokens:
                    can_end = True
            
                if can_end == True:
                    check_if_comment_next(tokens, orig_tokens, index)
            
            elif orig_tokens[index][-1] != "\n" and tokens[index+1][0] != "BTW":
                print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak or BTW expected after LOLCODE version!")
                return
            
            else:
                can_end = False
                
                # Start program if KTHXBYE is found
                if "KTHXBYE\n" in orig_tokens or "KTHXBYE" in orig_tokens:
                    can_end = True
            
                if can_end == True:
                    
                    statement(tokens, orig_tokens, index+1)          
                           
                else:
                    print_error("Error: KTHXBYE not found!")
                    return
        
        # Version not found
        else:
            
            if tokens[index+1][0] == "BTW" or tokens[index+1][0] == "OBTW":
                can_end = False
                
                # Start program if KTHXBYE is found
                if "KTHXBYE\n" in orig_tokens or "KTHXBYE" in orig_tokens:
                    can_end = True
            
                if can_end == True:
                    check_if_comment_next(tokens, orig_tokens, index)

            elif orig_tokens[index][-1] != "\n" and tokens[index+1][0] != "BTW":
                print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak or BTW expected after HAI!")
                return
            
            else:
                can_end = False

                # Start program if KTHXBYE is found
                if "KTHXBYE\n" in orig_tokens or "KTHXBYE" in orig_tokens:
                    can_end = True
            
                if can_end == True:
                    
                    statement(tokens, orig_tokens, index+1)          
                           
                else:
                    print_error("Error: KTHXBYE not found!")
                    return
    else:
        print_error("Error: Cannot start program without HAI!")
        return

def check_if_end(tokens, orig_tokens, index):
    global print_stack, eval_bool, loop_eval, loop_bool, loop_end, im_outta_yr_line_num, im_in_yr_line_num
    temp_index = index

    # Update values of symbol table
    populate_table(symbol_table, symbols)

    while tokens[temp_index-1][2] == tokens[index][2]:
        temp_index -= 1
    
    
    # Check if printing in a single line is not yet done
    if tokens[temp_index][1] == "Output Keyword":
        if orig_tokens[index][-1] != "\n":
            prnt(tokens, orig_tokens, index+1)
        else:
            if eval_bool == True:
                output = ""
                for string in print_stack:
                    output = output + string

                # Print output to console
                print_error(output)

            if tokens[index+1][0] != "KTHXBYE":
                statement(tokens, orig_tokens, index+1)
    else:
        # For evaluating loops
        if loop_eval == True:

            loop_eval = False
            temp_index = index
            while True:
                temp_index -= 1
                if tokens[temp_index][0] == "TIL" or tokens[temp_index][0] == "WILE":
                    break
 
            if tokens[temp_index][0] == "TIL" and symbols["IT"] == "FAIL":
                loop_bool = True
                eval_bool = True
            elif tokens[temp_index][0] == "WILE" and symbols["IT"] == "WIN":
                loop_bool = True
                eval_bool = True
            else:
                index = loop_end + 1
                loop_bool = False
                im_outta_yr_line_num.pop(0)
                im_in_yr_line_num.pop()
                im_in_yr_line_num.pop()
                if orig_tokens[index][-1] != "\n":
                    if tokens[index+1][0] == "BTW":
                        sline_comment(tokens, orig_tokens, index)
                    elif tokens[index+1][0] == "OBTW":
                        mline_comment(tokens, orig_tokens, index)
                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": Comment or linebreak expected after end of statement!")
                        return

        if tokens[index+1][0] != "KTHXBYE":
            statement(tokens, orig_tokens, index+1)
        
        # KTHXBYE found
        else:
            end(tokens, orig_tokens, index+1)

# Ending statement
def end(tokens, orig_tokens, index):

    # KTHXBYE is found
    if orig_tokens[index] == "KTHXBYE\n":

        # Go to comments_after function if KTHXBYE is not the last token from the lexemes table
        if tokens[index][2] != tokens[-1][2]:
            comments_after(tokens, orig_tokens, index+1)
        
        # End code if not
        else:
            return

    # KTHXBYE does not have linebreak
    elif tokens[index][0] == "KTHXBYE" and orig_tokens[index] != "KTHXBYE\n":
        index += 1

        # BTW found
        if tokens[index][1] == "Single Line Comment Declaration":

            # Print error if BTW is the last token
            if tokens[index][0] == tokens[-1][0] and tokens[index][2] == tokens[-1][2]:
                print_error("Error at Line " + str(tokens[index][2]) + ": Single line comment expected!")
                return

            index += 1

            # Single line comment found
            if tokens[index][1] == "Single Line Comment":

                # Single line comment line number not the same with BTW
                if tokens[index][2] != tokens[index-1][2]:
                    print_error("Error at Line " + str(tokens[index][2]) + ": Single line comment expected at the same line with BTW!")
                    return 

                # Check if there are more comments after
                elif tokens[index][2] != tokens[-1][2]:
                    comments_after(tokens, orig_tokens, index+1)
                
                # Code ends here
                else:
                    return

        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak or BTW expected after KTHXBYE!")
            return 

def comments_after(tokens, orig_tokens, index):

    # BTW    
    if tokens[index][1] == "Single Line Comment Declaration":

        # Error if last token from the lexemes table
        if tokens[index][0] == tokens[-1][0] and tokens[index][2] == tokens[-1][2]:
            print_error("Error at Line " + str(tokens[index][2]) + ": Single line comment expected!")
            return

        index += 1

        # Single line comment
        if tokens[index][1] == "Single Line Comment":
            
            # Single line comment line number not the same with BTW
            if tokens[index][2] != tokens[index-1][2]:
                print_error("Error at Line " + str(tokens[index][2]) + ": Single line comment expected at the same line with BTW!")
                return
            
            # Run the function again if not the last token
            if tokens[index][2] != tokens[-1][2]:
                comments_after(tokens, orig_tokens, index+1)
            
            # End if last token
            else:
                return

    # OBTW
    elif tokens[index][0] == "OBTW":

        index += 1

        # Multi-line comment
        if tokens[index][1] == "Multi-Line Comment":

            # Error if last token
            if tokens[index][0] == tokens[-1][0] and tokens[index][2] == tokens[-1][2]:
                print_error("Error at Line " + str(tokens[index][2]) + ": TLDR expected!")
                return

            index += 1

            # TLDR
            if tokens[index][0] == "TLDR":

                # Error if TLDR is not standalone
                if orig_tokens[index][-1] != "\n":
                    print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak expected after TLDR!")
                    return

                # Run the function again if not the last token
                if tokens[index][2] != tokens[-1][2]:
                    comments_after(tokens, orig_tokens, index+1)
                
                # End code
                else:
                    return
    
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": BTW or OBTW expected after KTHXBYE!")
        return
    

# Multi-line comments
def mline_comment(tokens, orig_tokens, index):
    if tokens[index][1] == "Multi-Line Comment":
        index += 1
        
        if tokens[index][0] == "TLDR":
            if orig_tokens[index][-1] != "\n":
                print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak expected after TLDR!")
                return
            else:
                check_if_end(tokens, orig_tokens, index)
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": TLDR expected!")
            return
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Multi-line comment expected!")
        return

# Single line comments
def sline_comment(tokens, orig_tokens, index):
    index += 1

    # Check if single line comment
    if tokens[index][1] == "Single Line Comment":
        
        # Check for linebreak
        if orig_tokens[index][-1] != "\n":
            print_error("Error at Line " + str(tokens[index][2]) + ": Linebreak expected after single line comment!")
            return
        
        # Line number of single line comment declaration and single line comment are not equal
        elif tokens[index][2] != tokens[index-1][2]:
            print_error("Error at Line " + str(tokens[index-1][2]) + ": Single line comment expected at the same line with BTW!")
            return

        else:
            check_if_end(tokens, orig_tokens, index)

    # Invalid value of token
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": Single line comment expected!")
        return

# Comment after token checker
def check_if_comment_next(tokens, orig_tokens, index):

    if orig_tokens[index][-1] != "\n":
        index += 1

        # Check if single line comment is next
        if tokens[index][1] == "Single Line Comment Declaration":
            sline_comment(tokens, orig_tokens, index)
        
        # Multi-line comment is next
        elif tokens[index][0] == "OBTW":
            print_error("Error at Line " + str(tokens[index][2]) + ": Cannot add multi-line comment within the same line!")
            return
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Expected linebreak!")
            return
    
    else:
        check_if_end(tokens, orig_tokens, index)

# Statements
def statement(tokens, orig_tokens, index):
    global if_else_block, switch_block, switch_or_if_else_block, oic_line_num, omg_line_num, im_in_yr_line_num, im_outta_yr_line_num, eval_bool, switch_eval_bool
    global var_ident, print_stack, smoosh_str, print_bool, expression_stack, var_decl_bool, assignment_bool, get_var, arity_bool, arity_stack, break_bool, if_bool
    global loop_bool, loop_start, loop_end, loop_eval

    # Reset variables 
    print_stack = []
    smoosh_str = ""
    print_bool = False
    var_decl_bool = False
    assignment_bool = False
    arity_bool = False

    # For printing
    if tokens[index][1] == "Output Keyword":
        prnt(tokens, orig_tokens, index+1)

    # For getting input
    elif tokens[index][1] == "Input Keyword":
        inpt(tokens, orig_tokens, index+1)

    # Single line comment
    elif tokens[index][0] == "BTW":
        sline_comment(tokens, orig_tokens, index)

    # Multi-line comment
    elif tokens[index][0] == "OBTW":
        mline_comment(tokens, orig_tokens, index+1)
    
    # For assignment or reassignment operation
    elif tokens[index][1] == "Variable Identifier":
        var_ident = tokens[index][0]

        if var_ident not in symbols.keys():
            print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
            return

        index += 1
        if tokens[index][1] == "Assignment Operator":
            assignment(tokens, orig_tokens, index+1)
        elif tokens[index][1] == "Reassignment Operator":
            reassignment(tokens, orig_tokens, index)
        else:
            print_error("Error at Line " + str(tokens[index-1][2]) + ": R, IS NOW A, or R MAEK expected!")
            return

    # For variable declaration
    elif tokens[index][1] == "Variable Declaration":
        var_decl(tokens, orig_tokens, index+1)
    
    # For typecasting
    elif tokens[index][1] == "Typecast Operator":
        typecast(tokens, orig_tokens, index+1)
    
    # For concatenating
    elif tokens[index][1] == "Concatenation Operator":
        concat(tokens, orig_tokens, index+1)
    
    # For arithmetic operation
    elif tokens[index][1] == "Arithmetic Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
    
    # For infinite arity operation
    elif tokens[index][1] == "Infinite Arity Operator":
        check_arity_op(tokens, orig_tokens, index, 0)

    # For if-else
    elif tokens[index][1] == "If Delimiter":

        # Pop from OIC block and append to if-else block and switch or if-else block. Check if comment is next
        if len(oic_line_num) != 0:
            oic_line_num.pop()
            if_else_block.append(tokens[index][1])
            switch_or_if_else_block.append(tokens[index][1])
            check_if_comment_next(tokens, orig_tokens, index)

        # Print error if not found
        else:
            print_error("Error: OIC Expected!")
            return

    # If keyword is encountered and latest block is if delimiter or Else keyword is encountered and latest block is if keyword
    elif ((tokens[index][1] == "If Keyword" and len(if_else_block) != 0 and if_else_block[-1] == "If Delimiter") or
          (tokens[index][1] == "Else Keyword" and len(if_else_block) != 0 and if_else_block[-1] == "If Keyword")):

        # Append to block
        if_else_block.append(tokens[index][1])

        check_win = bool_operations(symbols["IT"])
        
        if eval_bool == True:
            if tokens[index][1] == "If Keyword" and check_win == "FAIL":
                eval_bool = False
                if_bool = False
            elif tokens[index][1] == "If Keyword" and check_win == "WIN":
                eval_bool = True
            elif tokens[index][1] == "If Keyword" and check_win == "NOOB":
                eval_bool = False
                if_bool = False
            elif tokens[index][1] == "Else Keyword" and if_bool == False:
                if_bool = True
                eval_bool = True
            else:
                eval_bool = False

        elif tokens[index][1] == "Else Keyword" and if_bool == False:
            if_bool = True
            eval_bool = True
        

        # Go to next statement
        check_if_comment_next(tokens, orig_tokens, index)

    # OIC is encountered
    elif tokens[index][1] == "If-Else or Switch-Case Delimiter":

        # Check if there are OICs left in the OIC block
        if len(switch_or_if_else_block) != 0:
            if switch_or_if_else_block[-1] == "If Delimiter":

                # If keyword not found within if else block, exit the program
                if "If Keyword" not in if_else_block:
                    print_error("Error: Invalid If-then statement!")
                    return
                
                if_else_block = []

                if_bool = True

            elif switch_or_if_else_block[-1] == "Switch-Case Delimiter":

                # Case keyword not found within the switch block, exit the program
                if "Case Keyword" not in switch_block:
                    print_error("Error: Invalid switch-case statement!")
                    return

                break_bool = False
                switch_eval_bool = False

                switch_block = []

            # Prompt if unexpected OIC is found (no If Delimiter or Switch-Case Delimiter found first)
            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Unexpected OIC detected!")
                return
        
        # Prompt error if unexpected OIC found (no If Delimiter or Switch-Case Delimiter to pair with)
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Unexpected OIC detected!")
            return
        
        eval_bool = True

        # Pop from Switch or If-else block and check if comment is next
        switch_or_if_else_block.pop()
        check_if_comment_next(tokens, orig_tokens, index)

    # OMG? found
    elif tokens[index][1] == "Switch-Case Delimiter":

        # Pop from OIC block and append to switch block and switch or if-else block. Check if comment is next
        if len(oic_line_num) != 0:
            oic_line_num.pop()
            switch_block.append(tokens[index][1])
            switch_or_if_else_block.append(tokens[index][1])
            check_if_comment_next(tokens, orig_tokens, index)

        # Print error if not found
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": OIC expected!")
            return   
    
    # OMG or OMGWTF found
    elif ((tokens[index][1] == "Case Keyword" and len(switch_block) != 0 and switch_block[-1] == "Switch-Case Delimiter") or 
          (tokens[index][1] == "Case Keyword" and len(switch_block) != 0 and switch_block[-1] == "Case Keyword") or
          (tokens[index][1] == "Default Case Keyword" and len(switch_block) != 0 and switch_block[-1] == "Case Keyword")):

        # Append to switch block
        switch_block.append(tokens[index][1])

        # If OMG
        if tokens[index][1] == "Case Keyword":

            # Append to OMG line num
            omg_line_num.append(tokens[index][2])

            index += 1

            # Digit or Boolean literal as argument, go next
            if tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
                
                # Cast Literal to NUMBR or NUMBAR
                if tokens[index][1] == "Literal":
                    if re.match(tokens[index][0], literals[0]):
                        tokens[index][0] = int(tokens[index][0])
                    else:
                        tokens[index][0] = float(tokens[index][0])

                # Make eval and switch eval to true of IT is equal to literal or boolean literal
                if break_bool == False:
                    if symbols["IT"] == tokens[index][0]:
                        eval_bool = True
                        switch_eval_bool = True
                    else:
                        eval_bool = False
                
            # String as argument
            elif tokens[index][1] == "String Delimiter":

                index += 1

                if tokens[index][1] == "Literal":
                    
                    if break_bool == False:
                        if symbols["IT"] == tokens[index][0]:
                            eval_bool = True
                            switch_eval_bool = True
                        else:
                            eval_bool = False
                        index += 1
                    if tokens[index][1] == "String Delimiter":
                        index = index
            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid argument for OMG!")
                return   

        else:
            if switch_eval_bool == False and if_bool == True:
                eval_bool = True
        # Go to next statement
        check_if_comment_next(tokens, orig_tokens, index)
    
    # Break keyword found
    elif tokens[index][1] == "Break Keyword":
        if eval_bool == True and switch_eval_bool == True:
            break_bool = True
            eval_bool = False

        # Check if valid
        if len(switch_block) != 0 and switch_block[-1] == "Case Keyword" and omg_line_num[-1] < tokens[index][2]:
            # Go to next statement
            check_if_comment_next(tokens, orig_tokens, index)
        elif len(im_in_yr_line_num) != 0 and im_in_yr_line_num[-1] < tokens[index][2] and switch_eval_bool == False:

            if loop_bool == True:
                loop_bool = False
                index = loop_end
                statement(tokens, orig_tokens, index)
            else:
                # Go to next statement
                check_if_comment_next(tokens, orig_tokens, index)
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Unexpected GTFO detected!")
            return
    
    # IM IN YR found
    elif tokens[index][0] == "IM IN YR":

        if loop_bool == False:
            eval_bool = False
            loop_start = index

        if len(im_outta_yr_line_num) != 0:
            # Add identifier and line number to im in yr list
            im_in_yr_line_num.append(tokens[index+1][0])
            im_in_yr_line_num.append(tokens[index][2])

            index += 1

            if tokens[index][1] == "Variable Identifier":
                
                index += 1

                if tokens[index][1] == "Increment Operator" or tokens[index][1] == "Decrement Operator":          

                    index += 1

                    if tokens[index][1] == "Loop Separator":

                        index += 1

                        if tokens[index][1] == "Variable Identifier":

                            if tokens[index][0] not in symbols.keys():
                                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                                return
                            

                            if eval_bool == True:
                                
                                if arith_operations(symbols[tokens[index][0]]) == "NOOB":
                                    print_error("Error at Line " + str(tokens[index][2]) + ": Cannot typecast expression!")
                                    return
                                
                                if loop_bool == True:
                                    var_loop = arith_operations(symbols[tokens[index][0]])

                                if tokens[index-2][1] == "Increment Operator":
                                    var_loop += 1
                                    symbols[tokens[index][0]] = var_loop
                                else:
                                    var_loop -= 1
                                    symbols[tokens[index][0]] = var_loop

                            elif eval_bool == False:
                                if arith_operations(symbols[tokens[index][0]]) == "NOOB":
                                    print_error("Error at Line " + str(tokens[index][2]) + ": Cannot typecast expression!")
                                    return

                                var_loop = arith_operations(symbols[tokens[index][0]])

                                if tokens[index-2][1] == "Increment Operator":
                                    symbols[tokens[index][0]] = var_loop - 1
                                else:
                                    symbols[tokens[index][0]] = var_loop + 1

                            index += 1
                            if tokens[index][1] == "FAIL Loop Repeater" or tokens[index][1] == "WIN Loop Repeater":
                                
                                if eval_bool == True:
                                    loop_eval = True
                                    
                                index += 1

                                # For arithmetic operation
                                if tokens[index][1] == "Arithmetic Operator":
                                    if eval_bool == True:
                                        expression_stack.append(tokens[index][0])
                                    arith_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
                                
                                # Boolean NOT operation
                                elif tokens[index][0] == "NOT":
                                    if eval_bool == True:
                                        expression_stack.append(tokens[index][0])
                                    not_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)

                                # For boolean operation
                                elif tokens[index][1] == "Boolean Operator":
                                    expression_stack.append(tokens[index][0])
                                    bool_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
                                
                                # For comparison operation
                                elif tokens[index][1] == "Comparison Operator":
                                    if eval_bool == True:
                                        expression_stack.append(tokens[index][0])
                                    comp_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
                                
                                # For infinite arity operation
                                elif tokens[index][1] == "Infinite Arity Operator":
                                    check_arity_op(tokens, orig_tokens, index, 0)
                                
                                else:
                                    print_error("Error at Line " + str(tokens[index][2]) + ": Expression expected!")
                                    return
                            
                            else:
                                print_error("Error at Line " + str(tokens[index][2]) + ": TIL or WILE expected!")
                                return
                        
                        else:
                            print_error("Error at Line " + str(tokens[index][2]) + ": Variable expected!")
                            return
                    
                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": YR expected!")
                        return
                        
                else:
                    print_error("Error at Line " + str(tokens[index][2]) + ": UPPIN or NERFIN expected!")
                    return
            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid variable name detected!")
                return

        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": IM OUTTA YR expected!")
            return
      
    # IM OUTTA YR found
    elif tokens[index][0] == "IM OUTTA YR":
        if eval_bool == False:
            loop_bool = True
        # Check if there is IM IN YR to pair with and line number is less than the current line number
        if len(im_in_yr_line_num) != 0 and im_in_yr_line_num[-1] < im_outta_yr_line_num[0]:

            # Pop the line number of IM IN YR
            im_in_yr_line_num.pop()
            
            index += 1

            # Check if label are the same
            if im_in_yr_line_num[-1] == tokens[index][0]:
                
                # Pop the label from IM IN YR list and pop the first index of IM OUTTA YR list. Check if comment is next
                im_in_yr_line_num.pop()
                    
                loop_end = index-1

                if loop_bool == True or eval_bool == False:
                    index = loop_start-1
                    eval_bool = True
                    while (tokens[index][1] == "Single Line Comment Declaration" or tokens[index][1] == "Single Line Comment"
                        or tokens[index][1] == "Multi-Line Comment" or tokens[index][1] == "Multi-Line Comment Delimiter"):
                        index -= 1
                    
                check_if_comment_next(tokens, orig_tokens, index)

            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Loop label does not match!")
                return
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Unexpected IM OUTTA YR detected!")
            return

    elif tokens[index][0] == "KTHXBYE":
         end(tokens, orig_tokens, index+1)
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid statement!")
        return

# Printing function
def prnt(tokens, orig_tokens, index):
    global print_stack, print_bool, expression_stack, eval_bool

    if eval_bool == True:
        print_bool = True

    if tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                print_stack.append(str(symbols[tokens[index][0]]))
        else:
            if eval_bool == True:
                print_stack.append(str(tokens[index][0]))
        if tokens[index+1][1] == "Single Line Comment Declaration" or tokens[index+1][0] == "OBTW":
            check_if_comment_next(tokens, orig_tokens, index)
        elif orig_tokens[index][-1] == "\n":
            check_if_end(tokens, orig_tokens, index)
        else:
            prnt(tokens, orig_tokens, index+1)

    elif tokens[index][1] == "String Delimiter":

        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                print_stack.append(str(tokens[index][0]))
            index += 1
            if tokens[index][1] == "String Delimiter":
                if tokens[index+1][1] == "Single Line Comment Declaration" or tokens[index+1][0] == "OBTW":
                    check_if_comment_next(tokens, orig_tokens, index)
                elif orig_tokens[index][-1] == "\n":
                    check_if_end(tokens, orig_tokens, index)
                else:
                    prnt(tokens, orig_tokens, index+1)

    # For arithmetic operation
    elif tokens[index][1] == "Arithmetic Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 1)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 1)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 1)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 1)

    # Infinite Arity
    elif tokens[index][1] == "Infinite Arity Operator":
        check_arity_op(tokens, orig_tokens, index, 1)
    
    # Concatenation
    elif tokens[index][1] == "Concatenation Operator":
        concat(tokens, orig_tokens, index+1)
    
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid arguments for VISIBLE!")
        return

# For input statements
def inpt(tokens, orig_tokens, index):
    global eval_bool
    # Check if identifier
    if tokens[index][1] == "Variable Identifier":
        if tokens[index][0] not in symbols.keys():
            print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
            return

        if eval_bool == True:
            symbols["IT"] = askstring("Input", "Input here: ")

            # Empty string if no input declared
            if symbols["IT"] == None:
                symbols["IT"] = ""

            symbols[tokens[index][0]] = symbols["IT"]
        check_if_comment_next(tokens, orig_tokens, index)
        
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": Variable expected!")
        return

# Assignment operation
def assignment(tokens, orig_tokens, index):
    global var_ident, expression_stack, assignment_bool, get_var, eval_bool

    if eval_bool == True:
        assignment_bool = True
        get_var = var_ident

    # Identifier found; check for comments
    if tokens[index][1] == "Variable Identifier":
        if tokens[index][0] in symbols.keys():
            if eval_bool == True:
                symbols[var_ident] = symbols[tokens[index][0]]
            check_if_comment_next(tokens, orig_tokens, index)
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
            return
    # String found; check for comments
    elif tokens[index][1] == "String Delimiter":
        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                symbols[var_ident] = tokens[index][0]
            index += 1
            if tokens[index][1] == "String Delimiter":
                check_if_comment_next(tokens, orig_tokens, index)
    
    elif tokens[index][1] == "Boolean Literal":
        if eval_bool == True:
            symbols[var_ident] = tokens[index][0]
        check_if_comment_next(tokens, orig_tokens, index)

    elif tokens[index][1] == "Literal":
        if eval_bool == True:
            if "." in tokens[index][0]:
                symbols[var_ident] = float(tokens[index][0])
            else:
                symbols[var_ident] = int(tokens[index][0])
        check_if_comment_next(tokens, orig_tokens, index)
    
    # For arithmetic operation
    elif tokens[index][1] == "Arithmetic Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)

    elif tokens[index][1] == "Infinite Arity Operator":
        check_arity_op(tokens, orig_tokens, index, 0)
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid assignment!")
        return

# Reassignment operation
def reassignment(tokens, orig_tokens, index):
    global var_ident, eval_bool

    # IS NOW A found
    if tokens[index][0] == "IS NOW A":
        index += 1

        # Reassign to a type literal
        if tokens[index][1] == "Type Literal":
            if eval_bool == True:
                if cast(var_ident, tokens[index][0], tokens[index][2]) == "invalid":
                    print_error("Error at Line " + str(tokens[index][2]) + ": Cannot typecast YARN to NUMBR or NUMBAR!")
                    return
                symbols[var_ident] = cast(var_ident, tokens[index][0], tokens[index][2])
            check_if_comment_next(tokens, orig_tokens, index)
        else:
            print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid typecasting!")
            return

    # R MAEK found
    elif tokens[index][0] == "R MAEK":

        index += 1
        if tokens[index][1] == "Variable Identifier":
            var_ident2 = tokens[index][0]

            if var_ident2 not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return

            index += 1
            if tokens[index][1] == "Typecast Separator" or tokens[index][1] == "Type Literal":

                if tokens[index][1] == "Typecast Separator":
                    index += 1

                # Reassign to a type literal
                if tokens[index][1] == "Type Literal":
                    if eval_bool == True:
                        if cast(var_ident2, tokens[index][0], tokens[index][2]) == "invalid":
                            print_error("Error at Line " + str(tokens[index][2]) + ": Cannot typecast YARN to NUMBR or NUMBAR!")
                            return
                        symbols[var_ident] = cast(var_ident2, tokens[index][0], tokens[index][2])
                    check_if_comment_next(tokens, orig_tokens, index)
                else:
                    print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid typecasting!")
                    return
            
            elif tokens[index][1] == "Type Literal":
                check_if_comment_next(tokens, orig_tokens, index)

            else:
                print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid typecasting!")
                return
        else:
            print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid typecasting!")
            return


# Variable declaration operation
def var_decl(tokens, orig_tokens, index):
    global expression_stack, var_decl_bool, get_var, eval_bool

    if eval_bool == True:
        var_decl_bool = True

    # Variable found
    if tokens[index][1] == "Variable Identifier":
        
        # Variable
        identifier = tokens[index][0]
        get_var = identifier

        # Error if variable already declared
        if identifier in symbols.keys():
            print_error("Error at Line " + str(tokens[index][2]) + ": Variable already declared!")
            return

        # Check if comment found; uninitialized variable
        if tokens[index+1][1] == "Single Line Comment Declaration" or tokens[index+1][0] == "OBTW" or orig_tokens[index][-1] == "\n":
            if eval_bool == True:
                symbols[identifier] = "NOOB"
            check_if_comment_next(tokens, orig_tokens, index)
        else:
            index += 1

            # Variable assignment found
            if tokens[index][1] == "Variable Assignment":

                index += 1
                
                # String
                if tokens[index][1] == "String Delimiter":
                    index += 1

                    if tokens[index][1] == "Literal":
                        if eval_bool == True:
                            symbols[identifier] = tokens[index][0]
                        index += 1
                        if tokens[index][1] == "String Delimiter":
                            check_if_comment_next(tokens, orig_tokens, index)

                # Identifier
                elif tokens[index][1] == "Variable Identifier":
                    if tokens[index][0] in symbols.keys():
                        if eval_bool == True:
                            symbols[identifier] = symbols[tokens[index][0]]
                        check_if_comment_next(tokens, orig_tokens, index)
                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                        return

                elif tokens[index][1] == "Boolean Literal" or tokens[index][0] == "NOOB":
                    if eval_bool == True:
                        symbols[identifier] = tokens[index][0]
                    check_if_comment_next(tokens, orig_tokens, index)

                elif tokens[index][1] == "Literal":
                    if eval_bool == True:
                        if "." in tokens[index][0]:
                            symbols[identifier] = float(tokens[index][0])
                        else:
                            symbols[identifier] = int(tokens[index][0])
                    check_if_comment_next(tokens, orig_tokens, index)
                
                # Concatenation
                elif tokens[index][1] == "Concatenation Operator":
                    concat(tokens, orig_tokens, index+1)

                # For arithmetic operation
                elif tokens[index][1] == "Arithmetic Operator":
                    if eval_bool == True:
                        expression_stack.append(tokens[index][0])
                    arith_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)

                # Boolean NOT operation
                elif tokens[index][0] == "NOT":
                    if eval_bool == True:
                        expression_stack.append(tokens[index][0])
                    not_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0) 

                # For boolean operation
                elif tokens[index][1] == "Boolean Operator":
                    if eval_bool == True:
                        expression_stack.append(tokens[index][0])
                    bool_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)
                
                # For comparison operation
                elif tokens[index][1] == "Comparison Operator":
                    if eval_bool == True:
                        expression_stack.append(tokens[index][0])
                    comp_op(tokens, orig_tokens, index+1, [tokens[index][1]], 0, 0)

                elif tokens[index][1] == "Infinite Arity Operator":
                    check_arity_op(tokens, orig_tokens, index, 0, 0)
                else:
                    print_error("Error at Line " + str(tokens[index][2]) + ": Assigned value invalid!")
                    return
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": Variable expected!")
        return

# Typecast operation
def typecast(tokens, orig_tokens, index):
    global eval_bool
    if tokens[index][1] == "Variable Identifier":
        var_ident = tokens[index][0]

        if var_ident not in symbols.keys():
            print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
            return

        index += 1
        if tokens[index][1] == "Typecast Separator" or tokens[index][1] == "Type Literal":
            
            if tokens[index][1] == "Typecast Separator":
                index += 1

            if tokens[index][1] == "Type Literal":
                if eval_bool == True:
                    if cast(var_ident, tokens[index][0], tokens[index][2]) == "invalid":
                        print_error("Error at Line " + str(tokens[index][2]) + ": Cannot typecast YARN to NUMBR or NUMBAR!")
                        return
                    symbols["IT"] = cast(var_ident, tokens[index][0], tokens[index][2])                    
                check_if_comment_next(tokens, orig_tokens, index)

        else:
            print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid typecasting!")
            return
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": Can only typecast a variable!")
        return

# For casting 
def cast(var, type_req, line_num):

    # NOOB
    if type_req == "NOOB":
        return "NOOB"

    # TROOF
    elif type_req == "TROOF":
        if symbols[var] == "" or symbols[var] == 0 or symbols[var] == 0.0 or symbols[var] == "NOOB":
            return "FAIL"
        else:
            return "WIN"

    # NUMBR
    elif type_req == "NUMBR":
        if type(symbols[var]) == int:
            return int(symbols[var])
        elif type(symbols[var]) == float:
            return int(symbols[var])
        elif symbols[var] == "WIN":
            return 1
        elif symbols[var] == "FAIL" or symbols[var] == "NOOB":
            return 0
        elif type(symbols[var]) == str:
            cast = False
            for pattern in literals:
                if re.match(pattern, symbols[var]):
                    cast = True
                    return int(float(symbols[var]))
            if cast == False:
                return "invalid"

    # NUMBAR
    elif type_req == "NUMBAR":
        if type(symbols[var]) == float:
            return float(symbols[var])
        elif type(symbols[var]) == int:
            return float(symbols[var])
        elif symbols[var] == "WIN":
            return 1.0
        elif symbols[var] == "FAIL" or symbols[var] == "NOOB":
            return 0.0
        elif type(symbols[var]) == str:
            cast = False
            for pattern in literals:
                if re.match(pattern, symbols[var]):
                    cast = True
                    return float(symbols[var])
            if cast == False:
                return "invalid"

    # YARN       
    elif type_req == "YARN":
        if type(symbols[var]) == int:
            return str(symbols[var])
        elif type(symbols[var]) == float:
            return str(round(symbols[var],2))
        elif symbols[var] == "NOOB":
            return ""
        elif type(symbols[var]) == str:
            return str(symbols[var])

# Concatenation operation
def concat(tokens, orig_tokens, index):
    global smoosh_str, print_bool, print_stack, eval_bool

    # Identifier or literal
    if tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                smoosh_str = smoosh_str + str(symbols[tokens[index][0]])
        else:
            if eval_bool == True:
                smoosh_str = smoosh_str + str(tokens[index][0])
        index += 1

        # If AN is found, concatenate more arguments
        if tokens[index][1] == "Literal or Identifier Separator":
            more_concat(tokens, orig_tokens, index)
        else:
            index -= 1

            if eval_bool == True:
                # Pass value of smoosh to IT
                symbols["IT"] = smoosh_str
            
                # Append to print stack if print is called at the same line
                if print_bool == True:
                    print_stack.append(smoosh_str)

            if (tokens[index+1][0] == "MKAY" and tokens[index+2][1] == "Single Line Comment Declaration") or orig_tokens[index+1] == "MKAY\n":
                index += 1
                if tokens[index][2] != tokens[index-1][2]:
                    print_error("Error at Line " + str(tokens[index][2]) + ": MKAY not found at the same line!")
                    return
                check_if_comment_next(tokens, orig_tokens, index)
            elif orig_tokens[index][-1] == "\n" or tokens[index+1][1] == "Single Line Comment Declaration":
                check_if_comment_next(tokens, orig_tokens, index)
            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid concatenation!")
                return
    
    # String
    elif tokens[index][1] == "String Delimiter":

        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                smoosh_str = smoosh_str + tokens[index][0]
            index += 1
            if tokens[index][1] == "String Delimiter":
                index += 1

                # If AN is found, concatenate more arguments
                if tokens[index][1] == "Literal or Identifier Separator":
                    more_concat(tokens, orig_tokens, index)
                else:
                    index -= 1
                    
                    if eval_bool == True:
                        # Pass value of smoosh to IT
                        symbols["IT"] = smoosh_str

                        # Append to print stack if print is called at the same line
                        if print_bool == True:
                            print_stack.append(smoosh_str)

                    if (tokens[index+1][0] == "MKAY" and tokens[index+2][1] == "Single Line Comment Declaration") or orig_tokens[index+1] == "MKAY\n":
                        index += 1
                        if tokens[index][2] != tokens[index-1][2]:
                            print_error("Error at Line " + str(tokens[index][2]) + ": MKAY not found at the same line!")
                            return
                        check_if_comment_next(tokens, orig_tokens, index)
                    elif orig_tokens[index][-1] == "\n" or tokens[index+1][1] == "Single Line Comment Declaration":
                        check_if_comment_next(tokens, orig_tokens, index)
                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid concatenation!")
                        return
    
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid concatenation detected!")
        return

# Extension for concatenation operation
def more_concat(tokens, orig_tokens, index):
    global smoosh_str, print_bool, print_stack, eval_bool

    # Check if AN
    if tokens[index][1] == "Literal or Identifier Separator":
        index += 1

        # Identifier or literal
        if tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
            if tokens[index][1] == "Variable Identifier":
                if tokens[index][0] not in symbols.keys():
                    print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                    return
                if eval_bool == True:
                    smoosh_str = smoosh_str + str(symbols[tokens[index][0]])
            else:
                smoosh_str = smoosh_str + str(tokens[index][0])

            # Single line comment is next
            if tokens[index+1][1] == "Single Line Comment Declaration":
                if eval_bool == True:
                    # Pass value of smoosh to IT
                    symbols["IT"] = smoosh_str

                    # Append to print stack if print is called at the same line
                    if print_bool == True:
                        print_stack.append(smoosh_str)

                check_if_comment_next(tokens, orig_tokens, index)
            
            # Concatenate more if it does not end here
            elif orig_tokens[index][-1] != "\n":
                index += 1

                # Check if AN is next before proceeding
                if tokens[index][1] == "Literal or Identifier Separator":
                    more_concat(tokens, orig_tokens, index)
                
                elif tokens[index][0] == "MKAY":
                    if tokens[index][2] == tokens[index-1][2]:
                        if eval_bool == True:
                            # Pass value of smoosh to IT
                            symbols["IT"] = smoosh_str

                            # Append to print stack if print is called at the same line
                            if print_bool == True:
                                print_stack.append(smoosh_str)

                        check_if_comment_next(tokens, orig_tokens, index)
                    else:
                        print_error("Error at Line " + str(tokens[index-1][2]) + ": MKAY not found at the same line!")
                        return
                else:
                    print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid concatenation detected!")
                    return
            
            # Check if ending statement is next
            else:
                if eval_bool == True:
                    # Pass value of smoosh to IT
                    symbols["IT"] = smoosh_str

                    # Append to print stack if print is called at the same line
                    if print_bool == True:
                        print_stack.append(smoosh_str)

                check_if_end(tokens, orig_tokens, index)

        # String
        elif tokens[index][1] == "String Delimiter":

            index += 1

            if tokens[index][1] == "Literal":
                if eval_bool == True:
                    smoosh_str = smoosh_str + str(tokens[index][0])
                index += 1
                if tokens[index][1] == "String Delimiter":

                    # Singe line comment is next
                    if tokens[index+1][1] == "Single Line Comment Declaration":
                        if eval_bool == True:
                            # Pass value of smoosh to IT
                            symbols["IT"] = smoosh_str

                            # Append to print stack if print is called at the same line
                            if print_bool == True:
                                print_stack.append(smoosh_str)

                        check_if_comment_next(tokens, orig_tokens, index)
                    
                    # Concatenate more if it does not end here
                    elif orig_tokens[index][-1] != "\n":
                        index += 1

                        # Check if AN is next before proceeding
                        if tokens[index][1] == "Literal or Identifier Separator":
                            more_concat(tokens, orig_tokens, index)
                        elif tokens[index][0] == "MKAY":
                            if tokens[index][2] == tokens[index-1][2]:
                                if eval_bool == True:
                                    # Pass value of smoosh to IT
                                    symbols["IT"] = smoosh_str

                                    # Append to print stack if print is called at the same line
                                    if print_bool == True:
                                        print_stack.append(smoosh_str)

                                check_if_comment_next(tokens, orig_tokens, index)
                            else:
                                print_error("Error at Line " + str(tokens[index-1][2]) + ": MKAY not found at the same line!")
                                return
                        else:
                            print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid concatenation detected!")
                            return
                    
                    # Ending statement
                    else:
                        if eval_bool == True:
                            # Pass value of smoosh to IT
                            symbols["IT"] = smoosh_str

                            # Append to print stack if print is called at the same line
                            if print_bool == True:
                                print_stack.append(smoosh_str)

                        check_if_end(tokens, orig_tokens, index)
                        
        else:
            print_error("Error at Line " + str(tokens[index-1][2]) + ": Invalid concatenation detected!")
            return

# Arithmetic operation
def arith_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, eval_bool
    # Check for the following operators and do its function and increment its corresponding counter by 1
    # For arithmetic operation
    if tokens[index][1] == "Arithmetic Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # String is found, check if AN is found for arithmetic
    elif tokens[index][1] == "String Delimiter":

        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            index += 1
            if tokens[index][1] == "String Delimiter":
                an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
            
    # Identifier is found, check if AN is found for arithmetic
    elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                expression_stack.append(symbols[tokens[index][0]])
        else:
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
        an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arithmetic operation detected!")
        return

# Extension to arithmetic operation
def an_arith_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, arity_stack, eval_bool
    # AN is found and arith count is not equal to 0; decrement arith count by 1
    if tokens[index][1] == "Literal or Identifier Separator" and stack_operations[-1] == "Arithmetic Operator":
        
        stack_operations.pop()

        index += 1

        # Check for the following operators to do its function and add operation to stack
        # For arithmetic operation
        if tokens[index][1] == "Arithmetic Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # Boolean NOT operation
        elif tokens[index][0] == "NOT":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

        # For boolean operation
        elif tokens[index][1] == "Boolean Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # For comparison operation
        elif tokens[index][1] == "Comparison Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

        # String found
        elif tokens[index][1] == "String Delimiter":
            index += 1
            if tokens[index][1] == "Literal":
                if eval_bool == True:
                    expression_stack.append(tokens[index][0])
                index += 1
                if tokens[index][1] == "String Delimiter":

                    # Single line comment is next
                    if tokens[index+1][1] == "Single Line Comment Declaration":
                        if eval_bool == True:
                            if evaluate_expression(expression_stack, tokens[index][2]) == False:
                                return
                        check_if_comment_next(tokens, orig_tokens, index)
                    
                    # Check if stack is empty
                    elif len(stack_operations) == 0:
                        if eval_bool == True:
                            if evaluate_expression(expression_stack, tokens[index][2]) == False:
                                return
                        # If infinite arity
                        if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                            an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        # Next is MKAY
                        elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                            if eval_bool == True:
                                if evaluate_arity(arity_stack, tokens[index][2]) == False:
                                    return
                            check_if_comment_next(tokens, orig_tokens, index+1)

                        # Identifier, Literal, or String is found and VISIBLE is found in the same line, go to Output statement
                        elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                            tokens[index][1] == "String Delimiter") and print_before == 1):
                            
                            if orig_tokens[index][-1] == "\n":
                                check_if_end(tokens, orig_tokens, index)

                            elif tokens[index+1][1] == "Single Line Comment Declaration":
                                check_if_comment_next(tokens, orig_tokens, index)

                            else:
                                prnt(tokens, orig_tokens, index+1)

                        # Go next
                        else:
                            check_if_comment_next(tokens, orig_tokens, index)
                    
                    # AN is found; do the function again
                    elif tokens[index+1][1] == "Literal or Identifier Separator":

                        if stack_operations[-1] == "Comparison Operator":
                            an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        elif stack_operations[-1] == "Arithmetic Operator":
                            an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        elif stack_operations[-1] == "Boolean Operator":
                            an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": AN expected!")
                        return

        # Identifier or literal found
        elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
            if tokens[index][1] == "Variable Identifier":
                if tokens[index][0] not in symbols.keys():
                    print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                    return
                if eval_bool == True:
                    expression_stack.append(symbols[tokens[index][0]])
            else:
                if eval_bool == True:
                    expression_stack.append(tokens[index][0])
            # Single line comment is next
            if tokens[index+1][1] == "Single Line Comment Declaration":
                if eval_bool == True:
                    if evaluate_expression(expression_stack, tokens[index][2]) == False:
                        return
                check_if_comment_next(tokens, orig_tokens, index)
            
            # Check if stack is empty
            elif len(stack_operations) == 0:

                if eval_bool == True:
                    if evaluate_expression(expression_stack, tokens[index][2]) == False:
                        return
                # If infinite arity
                if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                    an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                # Next is MKAY
                elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                    if eval_bool == True:
                        if evaluate_arity(arity_stack, tokens[index][2]) == False:
                            return
                    check_if_comment_next(tokens, orig_tokens, index+1)

                # Identifier, Literal, or String is found and VISIBLE is found in the same line, go to Output statement
                elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                    tokens[index][1] == "String Delimiter") and print_before == 1):

                    if orig_tokens[index][-1] == "\n":
                        check_if_end(tokens, orig_tokens, index)

                    elif tokens[index+1][1] == "Single Line Comment Declaration":
                        check_if_comment_next(tokens, orig_tokens, index)
                            
                    else:
                        prnt(tokens, orig_tokens, index+1)

                # Go next
                else:
                    check_if_comment_next(tokens, orig_tokens, index)
            
            # AN is found; do the function again
            elif tokens[index+1][1] == "Literal or Identifier Separator":

                if stack_operations[-1] == "Comparison Operator":
                    an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                elif stack_operations[-1] == "Arithmetic Operator":
                    an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                elif stack_operations[-1] == "Boolean Operator":
                    an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                    
            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arithmetic operation detected!")
                return
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arithmetic operation detected!")
            return
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": AN expected!")
        return

# NOT Boolean operation
def not_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, arity_stack, eval_bool
    stack_operations.pop()

    # Arithmetic operation
    if tokens[index][1] == "Arithmetic Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # String found
    elif tokens[index][1] == "String Delimiter":
        index += 1
        if tokens[index][1] == "Literal":
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            index += 1
            if tokens[index][1] == "String Delimiter":

                # Single line comment is next
                if tokens[index+1][1] == "Single Line Comment Declaration":
                    if eval_bool == True:
                        if evaluate_expression(expression_stack, tokens[index][2]) == False:
                            return
                    check_if_comment_next(tokens, orig_tokens, index)
                
                # Check if stack is empty
                elif len(stack_operations) == 0:
                    if eval_bool == True:
                        if evaluate_expression(expression_stack, tokens[index][2]) == False:
                            return
                    # If infinite arity
                    if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                        an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

                    # Next is MKAY
                    elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                        if eval_bool == True:
                            if evaluate_arity(arity_stack, tokens[index][2]) == False:
                                return
                        check_if_comment_next(tokens, orig_tokens, index+1)

                    # Identifier, Literal, or String is found and VISIBLE is found within the same line, go to Output statement
                    elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                        tokens[index][1] == "String Delimiter") and print_before == 1):
                        
                        if orig_tokens[index][-1] == "\n":
                            check_if_end(tokens, orig_tokens, index)

                        elif tokens[index+1][1] == "Single Line Comment Declaration":
                            check_if_comment_next(tokens, orig_tokens, index)
                                
                        else:
                            prnt(tokens, orig_tokens, index+1)

                    # Go next
                    else:
                        check_if_comment_next(tokens, orig_tokens, index)
                
                # AN is found; do the function again
                elif tokens[index+1][1] == "Literal or Identifier Separator":
                    if stack_operations[-1] == "Comparison Operator":
                        an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                    
                    elif stack_operations[-1] == "Arithmetic Operator":
                        an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                    
                    elif stack_operations[-1] == "Boolean Operator":
                        an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                else:
                    print_error("Error at Line " + str(tokens[index][2]) + ": Invalid boolean operation detected!")
                    return
    
    # Identifier or literal found
    elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                expression_stack.append(symbols[tokens[index][0]])
        else:
            if eval_bool == True:
                expression_stack.append(tokens[index][0])

        # Single line comment is next
        if tokens[index+1][1] == "Single Line Comment Declaration":
            if eval_bool == True:
                if evaluate_expression(expression_stack, tokens[index][2]) == False:
                    return
            check_if_comment_next(tokens, orig_tokens, index)
        
        # Check if stack is empty
        elif len(stack_operations) == 0:
            if eval_bool == True:
                if evaluate_expression(expression_stack, tokens[index][2]) == False:
                    return
            # If infinite arity
            if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
            
            # Next is MKAY
            elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                if eval_bool == True:
                    if evaluate_arity(arity_stack, tokens[index][2]) == False:
                        return
                check_if_comment_next(tokens, orig_tokens, index+1)
            
            # Identifier, Literal, or String is found, go to Output statement
            elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                tokens[index][1] == "String Delimiter") and print_before == 1):

                if orig_tokens[index][-1] == "\n":
                    check_if_end(tokens, orig_tokens, index)

                elif tokens[index+1][1] == "Single Line Comment Declaration":
                    check_if_comment_next(tokens, orig_tokens, index)
                        
                else:
                    prnt(tokens, orig_tokens, index+1)

            # Go next
            else:
                check_if_comment_next(tokens, orig_tokens, index)

        # AN is found; do the function again
        elif tokens[index+1][1] == "Literal or Identifier Separator":

            if stack_operations[-1] == "Comparison Operator":
                an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
            
            elif stack_operations[-1] == "Arithmetic Operator":
                an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
            
            elif stack_operations[-1] == "Boolean Operator":
                an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Invalid boolean operation detected!")
            return
    
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid boolean operation detected!")
        return

# Boolean operation
def bool_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, eval_bool
    # Check for the following operators and do its function
    # For arithmetic operation
    if tokens[index][1] == "Arithmetic Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # Identifier or literal found, check if AN is found for boolean operator
    elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                expression_stack.append(symbols[tokens[index][0]])
        else:
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
        an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # String found, check if AN is found for boolean operator
    elif tokens[index][1] == "String Delimiter":
        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            index += 1
            if tokens[index][1] == "String Delimiter":
                an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid boolean operation detected!")
        return

# Extension to boolean operation      
def an_bool_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, arity_stack, eval_bool
    # AN is found and bool count is not equal to 0 or NOT is previous boolean operator; decrement bool count by 1
    if tokens[index][1] == "Literal or Identifier Separator" and stack_operations[-1] == "Boolean Operator":
        
        stack_operations.pop()
        
        index += 1

        # For arithmetic operation
        if tokens[index][1] == "Arithmetic Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # Boolean NOT operation
        elif tokens[index][0] == "NOT":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

        # For boolean operation
        elif tokens[index][1] == "Boolean Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # For comparison operation
        elif tokens[index][1] == "Comparison Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # String found
        elif tokens[index][1] == "String Delimiter":
            index += 1
            if tokens[index][1] == "Literal":
                if eval_bool == True:
                    expression_stack.append(tokens[index][0])
                index += 1
                if tokens[index][1] == "String Delimiter":

                    # Single line comment is next
                    if tokens[index+1][1] == "Single Line Comment Declaration":
                        if eval_bool == True:
                            if evaluate_expression(expression_stack, tokens[index][2]) == False:
                                return
                        check_if_comment_next(tokens, orig_tokens, index)
                    
                    # Check if stack is empty
                    elif len(stack_operations) == 0:
                        if eval_bool == True:
                            if evaluate_expression(expression_stack, tokens[index][2]) == False:
                                return
                        # If infinite arity
                        if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                            an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        # Next is MKAY
                        elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                            if eval_bool == True:
                                if evaluate_arity(arity_stack, tokens[index][2]) == False:
                                    return
                            check_if_comment_next(tokens, orig_tokens, index+1)

                        # Identifier, Literal, or String is found and VISIBLE is found in the same line, go to Output statement
                        elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                            tokens[index][1] == "String Delimiter") and print_before == 1):
                            
                            if orig_tokens[index][-1] == "\n":
                                check_if_end(tokens, orig_tokens, index)

                            elif tokens[index+1][1] == "Single Line Comment Declaration":
                                check_if_comment_next(tokens, orig_tokens, index)
                                
                            else:
                                prnt(tokens, orig_tokens, index+1)

                        # Go next
                        else:
                            check_if_comment_next(tokens, orig_tokens, index)
                    
                    # AN is found; do the function again
                    elif tokens[index+1][1] == "Literal or Identifier Separator":

                        if stack_operations[-1] == "Comparison Operator":
                            an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        elif stack_operations[-1] == "Arithmetic Operator":
                            an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        elif stack_operations[-1] == "Boolean Operator":
                            an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": AN expected!")
                        return
        
        # Identifier or literal found
        elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
            if tokens[index][1] == "Variable Identifier":
                if tokens[index][0] not in symbols.keys():
                    print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                    return
                if eval_bool == True:
                    expression_stack.append(symbols[tokens[index][0]])
            else:
                if eval_bool == True:
                    expression_stack.append(tokens[index][0])
            # Single line comment is next
            if tokens[index+1][1] == "Single Line Comment Declaration":
                if eval_bool == True:
                    if evaluate_expression(expression_stack, tokens[index][2]) == False:
                        return
                check_if_comment_next(tokens, orig_tokens, index)
            
            # Check if stack is empty
            elif len(stack_operations) == 0:
                if eval_bool == True:
                    if evaluate_expression(expression_stack, tokens[index][2]) == False:
                        return
                # If infinite arity
                if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                    an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                # Next is MKAY
                elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                    if eval_bool == True:
                        if evaluate_arity(arity_stack, tokens[index][2]) == False:
                            return
                    check_if_comment_next(tokens, orig_tokens, index+1)
                
                # Identifier, Literal, or String is found and VISIBLE is found within the same line, go to Output statement
                elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                    tokens[index][1] == "String Delimiter") and print_before == 1):

                    if orig_tokens[index][-1] == "\n":
                        check_if_end(tokens, orig_tokens, index)

                    elif tokens[index+1][1] == "Single Line Comment Declaration":
                        check_if_comment_next(tokens, orig_tokens, index)
                            
                    else:
                        prnt(tokens, orig_tokens, index+1)

                # Go next
                else:
                    check_if_comment_next(tokens, orig_tokens, index)
            
            # AN is found; do the function again
            elif tokens[index+1][1] == "Literal or Identifier Separator":

                if stack_operations[-1] == "Comparison Operator":
                    an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                elif stack_operations[-1] == "Arithmetic Operator":
                    an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                elif stack_operations[-1] == "Boolean Operator":
                    an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid boolean operation detected!")
                return
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Invalid boolean operation detected!")
            return
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": AN expected!")
        return

# Comparison operation
def comp_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, eval_bool
    # Check for operators and increment its corresponding count and do its function
    # For arithmetic operation
    if tokens[index][1] == "Arithmetic Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        stack_operations.append(tokens[index][1])
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    # Identifier or literal is found, check if AN is found for comparison operator
    elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                expression_stack.append(symbols[tokens[index][0]])
        else:
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
        an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
    
    # String is found, check if AN is found for comparison operator
    elif tokens[index][1] == "String Delimiter":
        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            index += 1
            if tokens[index][1] == "String Delimiter":
                an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid comparison operation detected!")
        return

# Extension to comparison opereation     
def an_comp_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, arity_stack, eval_bool

    # AN or Comparison Operator is found and comp count is not equal to 0; decrement comp count by 1 if AN is found
    if tokens[index][1] == "Literal or Identifier Separator" and stack_operations[-1] == "Comparison Operator":

        stack_operations.pop()

        index += 1

        # Check for the following operators and do its function
        # For arithmetic operation
        if tokens[index][1] == "Arithmetic Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # Boolean NOT operation
        elif tokens[index][0] == "NOT":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

        # For boolean operation
        elif tokens[index][1] == "Boolean Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # For comparison operation
        elif tokens[index][1] == "Comparison Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # String found
        elif tokens[index][1] == "String Delimiter":
            index += 1
            if tokens[index][1] == "Literal":
                if eval_bool == True:
                    expression_stack.append(tokens[index][0])
                index += 1
                if tokens[index][1] == "String Delimiter":

                    # Single line comment is next
                    if tokens[index+1][1] == "Single Line Comment Declaration":
                        if eval_bool == True:
                            if evaluate_expression(expression_stack, tokens[index][2]) == False:
                                return
                        check_if_comment_next(tokens, orig_tokens, index)
                    
                    # Check if stack is empty
                    elif len(stack_operations) == 0:
                        if eval_bool == True:
                            if evaluate_expression(expression_stack, tokens[index][2]) == False:
                                return
                        # If infinite arity
                        if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                            an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

                        # Next is MKAY
                        elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                            if eval_bool == True:
                                if evaluate_arity(arity_stack, tokens[index][2]) == False:
                                    return
                            check_if_comment_next(tokens, orig_tokens, index+1)

                        # Identifier, Literal, or String is found, go to Output statement
                        elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                            tokens[index][1] == "String Delimiter") and print_before == 1):
                            
                            if orig_tokens[index][-1] == "\n":

                                check_if_end(tokens, orig_tokens, index)

                            elif tokens[index+1][1] == "Single Line Comment Declaration":
                                check_if_comment_next(tokens, orig_tokens, index)
                                
                            else:
                                prnt(tokens, orig_tokens, index+1)

                        # Go next
                        else:
                            check_if_comment_next(tokens, orig_tokens, index)
                    
                    # AN is found; do the function again
                    elif tokens[index+1][1] == "Literal or Identifier Separator":
                        if stack_operations[-1] == "Comparison Operator":
                            an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        elif stack_operations[-1] == "Arithmetic Operator":
                            an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                        
                        elif stack_operations[-1] == "Boolean Operator":
                            an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                    
                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid comparsion operation detected!")
                        return
        
        # Identifier or literal found
        elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
            if tokens[index][1] == "Variable Identifier":
                if tokens[index][0] not in symbols.keys():
                    print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                    return
                if eval_bool == True:
                    expression_stack.append(symbols[tokens[index][0]])
            else:
                if eval_bool == True:
                    expression_stack.append(tokens[index][0])
            # Single line comment is next
            if tokens[index+1][1] == "Single Line Comment Declaration":
                if eval_bool == True:
                    if evaluate_expression(expression_stack, tokens[index][2]) == False:
                        return
                check_if_comment_next(tokens, orig_tokens, index)
            
            # Check if stack is empty
            elif len(stack_operations) == 0:
                if eval_bool == True:
                    if evaluate_expression(expression_stack, tokens[index][2]) == False:
                        return
                # If infinite arity
                if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:
                   an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                # Next is MKAY
                elif tokens[index+1][1] == "Infinite Arity Delimiter" and is_arity == 1:
                    if eval_bool == True:
                        if evaluate_arity(arity_stack, tokens[index][2]) == False:
                            return
                    check_if_comment_next(tokens, orig_tokens, index+1)
                
                # Identifier, Literal, or String is found, go to Output statement
                elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                      tokens[index][1] == "String Delimiter") and print_before == 1):
                    
                    if orig_tokens[index][-1] == "\n":
                        check_if_end(tokens, orig_tokens, index)

                    elif tokens[index+1][1] == "Single Line Comment Declaration":
                        check_if_comment_next(tokens, orig_tokens, index)
                            
                    else:
                        prnt(tokens, orig_tokens, index+1)

                # Go next
                else:
                    check_if_comment_next(tokens, orig_tokens, index)

            # AN is found; do the function again
            elif tokens[index+1][1] == "Literal or Identifier Separator":

                if stack_operations[-1] == "Comparison Operator":
                    an_comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                elif stack_operations[-1] == "Arithmetic Operator":
                    an_arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
                
                elif stack_operations[-1] == "Boolean Operator":
                    an_bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
            
            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid comparison operation detected!")
                return
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Invalid comparsion operation detected!")
            return
    else:
        print_error("Error at Line " + str(tokens[index-1][2]) + ": AN expected!")
        return

def evaluate_expression(exp_stack, line_num):
    global print_bool, var_decl_bool, assignment_bool, print_stack, arity_bool, arity_stack
    expressions = [
        "SUM OF" 
        , "DIFF OF"
        , "PRODUKT OF"
        , "QUOSHUNT OF"
        , "MOD OF"
        , "BIGGR OF"
        , "SMALLR OF"
        , "BOTH OF"
        , "EITHER OF"
        , "WON OF"
        , "NOT"
        , "BOTH SAEM"
        , "DIFFRINT"
    ]

    ops = [
        "SUM OF" 
        , "DIFF OF"
        , "PRODUKT OF"
        , "QUOSHUNT OF"
        , "MOD OF"
        , "BIGGR OF"
        , "SMALLR OF"
    ]

    evaluate = []
    while(len(exp_stack)) != 0:

        while exp_stack[-1] not in expressions:
            evaluate.append(exp_stack.pop())
        evaluate.append(exp_stack.pop())

        # Arithmetic
        if evaluate[-1] in ops:
            op1 = arith_operations(evaluate[-2])
            op2 = arith_operations(evaluate[-3])
            # Throw error if invalid operand
            if op1 == "NOOB" or op2 == "NOOB":
                print_error("Error at Line " + str(line_num) + ": Cannot typecast operand!")
                return False

            result = 0

            if evaluate[-1] == "SUM OF":
                result = op1 + op2
            elif evaluate[-1] == "DIFF OF":
                result = op1 - op2
            elif evaluate[-1] == "PRODUKT OF":
                result = op1 * op2
            elif evaluate[-1] == "QUOSHUNT OF":
                if type(op1) == float or type(op2) == float:
                    result = op1 / op2
                else:
                    result = op1 // op2
            elif evaluate[-1] == "MOD OF":
                result = op1 % op2
            elif evaluate[-1] == "BIGGR OF":
                result = max(op1, op2)
            elif evaluate[-1] == "SMALLR OF":
                result = min(op1, op2)
            
            # Pass value to IT
            symbols["IT"] = result

            evaluate.pop()
            evaluate.pop()
            evaluate.pop()

        # Boolean
        elif evaluate[-1] == "BOTH OF" or evaluate[-1] == "EITHER OF" or evaluate[-1] == "WON OF":
            op1 = bool_operations(evaluate[-2])
            op2 = bool_operations(evaluate[-3])

            result = ""

            # Throw error if invalid operand
            if op1 == "NOOB" or op2 == "NOOB":
                print_error("Error at Line " + str(line_num) + ": Cannot typecast operand!")
                return False

            if evaluate[-1] == "BOTH OF":
                if op1 == "FAIL" or op2 == "FAIL":
                    result = "FAIL"
                else:
                    result = "WIN"
            elif evaluate[-1] == "EITHER OF":
                if op1 == "WIN" or op2 == "WIN":
                    result = "WIN"
                else:
                    result = "FAIL"
            elif evaluate[-1] == "WON OF":
                if op1 == op2:
                    result = "FAIL"
                else:
                    result = "WIN"
            
            # Pass value to IT
            symbols["IT"] = result

            evaluate.pop()
            evaluate.pop()
            evaluate.pop()

        # Comparison
        elif evaluate[-1] == "BOTH SAEM" or evaluate[-1] == "DIFFRINT":
            op1 = arith_operations(evaluate[-2])
            op2 = arith_operations(evaluate[-3])

            result = ""

            # Throw error if invalid operand
            if op1 == "NOOB" or op2 == "NOOB":
                print_error("Error at Line " + str(line_num) + ": Cannot typecast operand!")
                return False
            
            if evaluate[-1] == "BOTH SAEM":
                if op1 == op2:
                    result = "WIN"
                else:
                    result = "FAIL"

            elif evaluate[-1] == "DIFFRINT":
                if op1 == op2:
                    result = "FAIL"
                else:
                    result = "WIN"

            # Pass value to IT
            symbols["IT"] = result

            evaluate.pop()
            evaluate.pop()
            evaluate.pop()

        # NOT operator
        elif evaluate[-1] == "NOT":

            evaluate.pop()

            if evaluate[-1] == "" or evaluate[-1] == 0 or evaluate[-1] == 0.0 or evaluate[-1] == "FAIL":
                symbols["IT"] = "WIN"
            else:
                symbols["IT"] = "FAIL"
            
            evaluate.pop()
        
        if len(exp_stack) != 0:
            exp_stack.append(symbols["IT"])

    if arity_bool == False:
        if print_bool == True:
            print_stack.append(str(symbols["IT"]))
        if var_decl_bool == True:
            symbols[get_var] = symbols["IT"]
        if assignment_bool == True:
            symbols[get_var] = symbols["IT"]
    else:
        arity_stack.append(symbols["IT"])


# For typecasting operands into integers or floats
def arith_operations(op):
    if op == "WIN":
        return 1
    elif op == "FAIL":
        return 0
    elif type(op) == int or type(op) == float:
        return op
    elif re.match(literals[0], op):
        return int(op)
    elif re.match(literals[1], op):
        return float(op)
    else:
        return "NOOB"

# For typecasting operands to boolean
def bool_operations(op):
    if op == "WIN" or op == "FAIL":
        return op
    elif op == "" or op == 0 or op == 0.0:
        return "FAIL"
    elif op == "NOOB":
        return "NOOB"
    else:
        return "WIN"

# Check arity operation
def check_arity_op(tokens, orig_tokens, index, print_before):
    global arity_stack, arity_bool, eval_bool

    # Pass value of index to temporary index
    temp_index = index

    # For taking note of current line number
    temp_index2 = index

    # MKAY found in original tokens
    if "MKAY" in orig_tokens or "MKAY\n" in orig_tokens:

        # Keep incrementing temp index by 1 until MKAY is found
        while tokens[temp_index][1] != "Infinite Arity Delimiter":
            temp_index += 1
        
        # Do arity operation if MKAY is within the same line number
        if tokens[index][2] == tokens[temp_index][2]:
            if eval_bool == True:
                arity_bool = True
                arity_stack.append(tokens[index][0])
            arity_op(tokens, orig_tokens, index+1, print_before)
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": MKAY expected in ANY OF or ALL OF at the same line!")
            return
    else:
        print_error("Error at Line " + str(tokens[temp_index2][2]) + ": MKAY not found!")
        return

# Arity operation
def arity_op(tokens, orig_tokens, index, print_before):
    global arity_stack, expression_stack, eval_bool

    # For arithmetic operation
    if tokens[index][1] == "Arithmetic Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        arith_op(tokens, orig_tokens, index+1, [tokens[index][1]], 1, print_before)
    
    # Boolean NOT operation
    elif tokens[index][0] == "NOT":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        not_op(tokens, orig_tokens, index+1, [tokens[index][1]], 1, print_before)

    # For boolean operation
    elif tokens[index][1] == "Boolean Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        bool_op(tokens, orig_tokens, index+1, [tokens[index][1]], 1, print_before)
    
    # For comparison operation
    elif tokens[index][1] == "Comparison Operator":
        if eval_bool == True:
            expression_stack.append(tokens[index][0])
        comp_op(tokens, orig_tokens, index+1, [tokens[index][1]], 1, print_before)

    elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
        if tokens[index][1] == "Variable Identifier":
            if tokens[index][0] not in symbols.keys():
                print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                return
            if eval_bool == True:
                arity_stack.append(symbols[tokens[index][0]])
        else:
            if eval_bool == True:
                arity_stack.append(tokens[index][0])
        if tokens[index+1][0] == "MKAY":
            index += 1
            if eval_bool == True:
                if evaluate_arity(arity_stack, tokens[index][2]) == False:
                    return
            check_if_comment_next(tokens, orig_tokens, index)
        else:
            an_arity_op(tokens, orig_tokens, index+1, [tokens[index][1]], 1, print_before)

    # String is found
    elif tokens[index][1] == "String Delimiter":
        index += 1

        if tokens[index][1] == "Literal":
            if eval_bool == True:
                arity_stack.append(tokens[index][0])
            index += 1
            if tokens[index][1] == "String Delimiter":
                if tokens[index+1][0] == "MKAY":
                    index += 1
                    if eval_bool == True:
                        if evaluate_arity(arity_stack, tokens[index][2]) == False:
                            return
                    check_if_comment_next(tokens, orig_tokens, index)
                else:
                    an_arity_op(tokens, orig_tokens, index+1, [tokens[index][1]], 1, print_before)
 
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arity operation detected!")
        return

# Arity operation extension
def an_arity_op(tokens, orig_tokens, index, stack_operations, is_arity, print_before):
    global expression_stack, arity_stack, eval_bool

    if tokens[index][1] == "Literal or Identifier Separator":

        index += 1

        # Check for the following operators and do its function
        # For arithmetic operation
        if tokens[index][1] == "Arithmetic Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            arith_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # Boolean NOT operation
        elif tokens[index][0] == "NOT":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            not_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

        # For boolean operation
        elif tokens[index][1] == "Boolean Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            bool_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # For comparison operation
        elif tokens[index][1] == "Comparison Operator":
            stack_operations.append(tokens[index][1])
            if eval_bool == True:
                expression_stack.append(tokens[index][0])
            comp_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)
        
        # String found
        elif tokens[index][1] == "String Delimiter":
            index += 1
            if tokens[index][1] == "Literal":
                if eval_bool == True:
                    arity_stack.append(tokens[index][0])
                index += 1
                if tokens[index][1] == "String Delimiter":

                    # AN is found; do the function again
                    if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:

                        an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

                    elif tokens[index+1][1] == "Infinite Arity Delimiter":
                        index += 1
                        if eval_bool == True:
                            if evaluate_arity(arity_stack, tokens[index][2]) == False:
                                return
                        check_if_comment_next(tokens, orig_tokens, index)

                    # Identifier, Literal, or String is found, go to Output statement
                    elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                        tokens[index][1] == "String Delimiter") and print_before == 1):
                        prnt(tokens, orig_tokens, index+1)

                    else:
                        print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arity operation detected!")
                        return
        
        # Identifier or literal found
        elif tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal":
            if tokens[index][1] == "Variable Identifier":
                if tokens[index][0] not in symbols.keys():
                    print_error("Error at Line " + str(tokens[index][2]) + ": Variable not found in symbol table!")
                    return
                if eval_bool == True:
                    arity_stack.append(symbols[tokens[index][0]])
            else:
                if eval_bool == True:
                    arity_stack.append(tokens[index][0])
            # AN is found; do the function again
            if tokens[index+1][1] == "Literal or Identifier Separator" and is_arity == 1:

                an_arity_op(tokens, orig_tokens, index+1, stack_operations, is_arity, print_before)

            elif tokens[index+1][1] == "Infinite Arity Delimiter":
                index += 1
                if eval_bool == True:
                    if evaluate_arity(arity_stack, tokens[index][2]) == False:
                        return
                check_if_comment_next(tokens, orig_tokens, index)
            
            # Identifier, Literal, or String is found, go to Output statement
            elif ((tokens[index][1] == "Variable Identifier" or tokens[index][1] == "Literal" or tokens[index][1] == "Boolean Literal" or 
                    tokens[index][1] == "String Delimiter") and print_before == 1):
                prnt(tokens, orig_tokens, index+1)

            else:
                print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arity operation detected!")
                return               
        else:
            print_error("Error at Line " + str(tokens[index][2]) + ": Invalid arity operation detected!")
            return
    
    else:
        print_error("Error at Line " + str(tokens[index][2]) + ": AN expected!")
        return

def evaluate_arity(arity_stack, line_num):
    global print_bool, var_decl_bool, assignment_bool, get_var

    evaluate = []

    # Get all operands and convert to bool
    while len(arity_stack) != 1:
        operand = bool_operations(arity_stack.pop())
        
        # Throw error if invalid operand
        if operand == "NOOB":
            print_error("Error at Line " + str(line_num) + ": Cannot typecast operand!")
            return False
        
        # Append for evaluation
        evaluate.append(operand)
    
    # ALL OF
    if arity_stack[0] == "ALL OF":
        if "FAIL" in evaluate:
            symbols["IT"] = "FAIL"
        else:
            symbols["IT"] = "WIN"

    # ANY OF
    elif arity_stack[0] == "ANY OF":
        if "WIN" in evaluate:
            symbols["IT"] = "WIN"
        else:
            symbols["IT"] = "FAIL"

    # Clean arity stack
    arity_stack.pop()

    if print_bool == True:
        print_stack.append(symbols["IT"])
    if var_decl_bool == True:
        symbols[get_var] = symbols["IT"]
    if assignment_bool == True:
        symbols[get_var] = symbols["IT"]


######################### G U I #########################

# Init tkinter window
root = Tk()
root.title("The Assassins' LOLTERPRETER")

# Maximize Window Size
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(str(w) + "x" + str(h))

# Init Main Frame
main_frame = Frame(root)
main_frame.pack(expand=True, fill=BOTH)
main_frame.pack_propagate(0)

### UPPER FRAME ###
upper_frame = Frame(main_frame)
upper_frame.pack()

# Init three frames for the upper frame
ul_frame = Frame(upper_frame)
um_frame = Frame(upper_frame)
ur_frame = Frame(upper_frame)

ul_frame.grid(row=0, column=0)
um_frame.grid(row=0, column=1, sticky="ns")
ur_frame.grid(row=0, column=2, sticky="ns")

### UPPER LEFT FRAME ###
# File Explorer
select_file_btn = Button(ul_frame, text="Select file..", command=select_file)
select_file_btn.pack(fill=X)

# Text Editor
text_editor = scrolledtext.ScrolledText(ul_frame, width=65, height=20)
text_editor.pack()

### UPPER MIDDLE FRAME (LEXEMES TABLE) ###
lexer_label = Label(um_frame, text="Lexemes") 
lexer_label.pack()

# Lexemes Table
lexer_table = ttk.Treeview(um_frame, show="headings")

# Lexemes Table Columns
lexer_table["columns"] = ("lexeme", "classification")

# Lexemes Table Headings
lexer_table.heading("lexeme", text="Lexeme")
lexer_table.heading("classification", text="Classification")

# Lexemes Table Scrollbar
lexer_scrollbar = ttk.Scrollbar(um_frame, orient=VERTICAL, command=lexer_table.yview)
lexer_table.configure(yscroll=lexer_scrollbar.set)
lexer_scrollbar.pack(fill=Y, side=RIGHT)

lexer_table.pack(expand=True, fill=BOTH)

### UPPER RIGHT FRAME (SYMBOL TABLE) ###
symbol_label = Label(ur_frame, text="Symbol Table") 
symbol_label.pack()

# Symbol Table
symbol_table = ttk.Treeview(ur_frame, show="headings")

# Symbol Table Columns
symbol_table["columns"] = ("identifier", "value")

# Symbol Table Headings
symbol_table.heading("identifier", text="Identifier")
symbol_table.heading("value", text="Value")

# Symbol Table Scrollbar
symbol_scrollbar = ttk.Scrollbar(ur_frame, orient=VERTICAL, command=symbol_table.yview)
symbol_table.configure(yscroll=symbol_scrollbar.set)
symbol_scrollbar.pack(fill=Y, side=RIGHT)

symbol_table.pack(expand=True, fill=BOTH)

### EXECUTE/RUN BUTTON ###
run_btn = Button(main_frame, text="EXECUTE", command=run)
run_btn.pack(pady=5, fill=X)

### CONSOLE ###
console = scrolledtext.ScrolledText(main_frame)
console.pack(expand=True, fill=BOTH)
console["state"] = "disabled"

### Start GUI here ###
root.mainloop()
