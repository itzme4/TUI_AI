def greeting():
    import time
    now=time.strftime("%H")
    if "5"<=now <="11":
        return "Good Morning"
    elif "12">= now <= "17":
        return "Good Afternoon"
    elif "18">= now <="21":
        return "Good Evening"
    else:
        return "Welcome Back"
