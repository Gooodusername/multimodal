# import pywebio
 
# from pywebio import start_server
# from pywebio.input import *
# from pywebio.output import *
# from pywebio.session import set_env, info as session_info
# # pywebio.input.slider("text",min_value=0,max_value=5)
# # pywebio.input.actions("返回",buttons="value",type="submit")

# def text():
#     con = actions('Confirm to delete file?', ['confirm', 'cancel'],
#                         help_text='Unrecoverable after file deletion')
#     put_markdown('You clicked the `%s` button' % con).show() 

# def t():
#     con = actions('Co?', ['confirm', 'cancel'],
#                         help_text='Unrecoverable after file deletion')
#     put_markdown('You clicked the `%s` button' % con).show() 

# def main():
#     t()
#     text()

# if __name__=="__main__":
#     main()
import pywebio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *

def main():
    put_row([
    put_column([
        put_code('A'),
        put_row([
            put_code('B1'), None,  
            put_code('B2'), None,
            put_code('B3'),
        ]),
        put_code('C'),
    ]), None,
    put_code('D'), None,
    put_code('E')
])

if __name__ == "__main__":
    main()


