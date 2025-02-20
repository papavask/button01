import streamlit as st
import logging



def get_remote_ip() -> str:
    """Get remote ip."""
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None
    return session_info.request.remote_ip


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_ip = get_remote_ip()
        return super().filter(record)



def click_btn01():
    st.session_state.button01_clicked = True
    st.session_state.Btn_Ena = True



def click_btn02():
    st.session_state.button02_clicked = True
    st.session_state.Btn_Ena = False
    
def start_main():
    #im = Image.open("./Source/favicon.ico")
# Configure the main page
    st.set_page_config(
        page_title="Test Buttons",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Report a bug': 'mailto:papavask@yahoo.com',
            'About': "# Just testng buttons"
        }
    )

# Set title
    st.title("Testing")

    subheader = st.subheader("Have Fun")

# Set text
    st.write("Welcome !!!")

    logger.info("In Main")

    cols = st.columns((2,2,10))

    if 'Btn_Ena' not in st.session_state:
        st.session_state.Btn_Ena = False
        logger.info("bp001")
        
    if 'Button01_clicked' not in st.session_state:
       st.session_state.button01_clicked = False
       logger.info("bp002")

    if 'Button02_clicked' not in st.session_state:
      st.session_state.button02_clicked = False
      logger.info("bp003")

    cols[0].button("Button01", on_click=click_btn01, disabled=st.session_state.Btn_Ena)
    cols[1].button("Button02", on_click=click_btn02, disabled=not st.session_state.Btn_Ena)

def init_logging():
    # Make sure to instanciate the logger only once
    # otherwise, it will create a StreamHandler at every run
    # and duplicate the messages

    # create a custom logger
    logger = logging.getLogger("logger")
    if logger.handlers:  # logger is already setup, don't setup again
        return
    logger.propagate = False
    logger.setLevel(logging.INFO)
    # in the formatter, use the variable "user_ip"
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s [user_ip=%(user_ip)s] - %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.addFilter(ContextFilter())
    handler.setFormatter(formatter)
    logger.addHandler(handler)


if __name__ == "__main__":
    init_logging()
    logger = logging.getLogger("logger")
    logger.info("Inside main")
    start_main()

