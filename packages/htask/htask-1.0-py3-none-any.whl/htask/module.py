#Some common task started

# [1] create fibnacci series 
def fib(num):
        a = 0
        b = 1
        for i in range(num):
            print(a)
            c = a + b
            a = b 
            b = c 

    # [2] Check if a string is a palindrome
def palindrome(name):
        a = str(name)
        b = a[::-1] 
      
        if a == b :
            print(f"[+] {a} is palindrome")
        else:
            print(f" [+] {b} is not palindrome")

    # [3] Reverse a string
def rev(String):
        a = str(String)
        print([a[::-1]]) 

    # [4] find duplicate element
def duplicate(arr):
        items = set()
        Duplicate_values = []

        for i in arr:
            if i in items:
                Duplicate_values.append(i)

            else:
                items.add(i)

        print(f"[+] Duplicate Values are - {Duplicate_values}")

# [+] Patterns tasks started

# [1] Right-Angled Triangle
def RAT(n:int, p:str):
        for i in range(1, n + 1):
            print(f"{p}" * i)


    # [2] Inverted Right-Angled Triangle
def IRAT(n,p):
        for i in range(n , 0, -1):
            print(f"{p}" * i)

    # [3] Pyramid
def PRM(n,p):
        for i in range(n):
            print(' ' * (n - 1 - i) + f'{p}' * (2 * i + 1))
    # [4] Inverse Pyramid
def IPRM(n,p):
        for i in range(n, 0, -1):
            print(' ' * (n - i)  + f'{p}' * (2 * i - 1))
        
    # [5] Diamond
def DIA(n,p):
       PRM(n,p)
       IPRM(n,p)
       
    # [6] Square
def SQR(n,p):
        for i in range(n):
            print(f'{p}' * n)
        
    # [7]  Hollow Square
def HSQR(n,p):
        for i in range(n):
            if i == 0 or i == n - 1:
                print(f'{p}' * n)
            else:
                print(f'{p}' + ' ' * (n - 2) + f'{p}')
    
    # [8] Hollow Triangle

def HTRI(n,p):
        for i in range(n):
            if i == n - 1:
                print(f'{p}' * (2 * n - 1))
            else:
                print(' ' * (n - i - 1) + f'{p}' + ' ' * (2 * i - 1) + (f'{p}' if i > 0 else ''))

    # [9] Pascal's Triangle
def HGLASS(n,p):
            # Print the upper half of the hourglass
        '''for i in range(n, 0, -1):
            print(' ' * (n - i) + '*' * (2 * i - 1))'''
        IPRM(n,p)
        
        # Print the lower half of the hourglass
        for i in range(2, n + 1):
            print(' ' * (n - i) + f'{p}' * (2 * i - 1))
            

