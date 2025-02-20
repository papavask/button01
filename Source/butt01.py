import streamlit as st
import logging
import pandas as pd
import asyncio



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


def click_btn01(Radio_url):
    st.session_state.Button01_clicked = True
    st.session_state.Btn01_Dis = True
    st.session_state.Btn02_Dis = False
    #asyncio.run(play(Radio_url))
    st.audio(Radio_url, format="audio/mp3", autoplay=True)

async def play(Station_url):
    st.audio(Station_url, format="audio/mp3", autoplay=True)


def click_btn02(Station_url):
    st.session_state.Button02_clicked = True
    st.session_state.Btn02_Dis = True
    st.audio(Station_url, format="audio/mp3", autoplay=True)
    
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

    if 'Btn01_Dis' not in st.session_state:
        st.session_state.Btn01_Dis = False
        logger.info("bp001")

    if 'Btn02_Dis' not in st.session_state:
        st.session_state.Btn02_Dis = True
        logger.info("bp001a")
        
    if 'Button01_clicked' not in st.session_state:
       st.session_state.Button01_clicked = False
       logger.info("bp002")

    if 'Button02_clicked' not in st.session_state:
      st.session_state.Button02_clicked = False
      logger.info("bp003")

    if 'Selected_station' not in st.session_state:
        st.session_state.Selected_station = ""

    file_path = "./Source/RadioList.csv"
    data = pd.read_csv(file_path, sep=",")
    station_list = list(data["Station"])
# Select station
    selected_station = st.sidebar.selectbox(
                       "Select a station from the list",
                       station_list
                       )
    Radio_url = data[data["Station"] == selected_station].values.tolist()[0][2][2:-1]
    
    if st.session_state.Selected_station != selected_station:
        st.session_state.Btn01_Dis = False
        st.session_state.Btn02_Dis = True
        st.session_state.Selected_station = selected_station
        
    st.write(st.session_state.Btn02_Dis)
    cols[0].button("Button01", on_click=click_btn01, args=[Radio_url], disabled=st.session_state.Btn01_Dis)
    cols[1].button("Button02", on_click=click_btn02, args=[Radio_url], disabled=st.session_state.Btn02_Dis)

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

