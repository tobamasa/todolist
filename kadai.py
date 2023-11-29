import streamlit as st
import pandas as pd
import datetime, time

# セッション状態を定義
'''
ここでは，タスクを保持するデータフレーム・カテゴリを保持するデータフレーム・直前に入力されたタスクを保持するlast_taskを定義
'''
if 'tasks_df' not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=["Task", "Deadline", "Priority", "Category"])
if 'category_df' not in st.session_state:
    st.session_state.category_df =  pd.DataFrame(columns=["Category"])
if 'last_task' not in st.session_state:
    st.session_state.last_task = ""

def show_category_page():
    '''
    カテゴリを自ら追加することが可能
    このカテゴリはメタ情報として利用可能
    '''
    # 入力を受け取る
    with st.form("input_form", clear_on_submit=True):
        input_category = st.text_input("追加するカテゴリを入力:")
        submitted = st.form_submit_button("追加")

    # 入力を受け取ったらDFに追加
    if submitted:
        new_category = pd.DataFrame({"Category": [input_category]})
        st.session_state.category_df = pd.concat([st.session_state.category_df, new_category], ignore_index=True)
        st.success("カテゴリが追加されました!")
    
    # カテゴリリストの表示
    st.subheader("カテゴリリスト:")
    if st.session_state.category_df.empty:
        st.info("現在、カテゴリはありません。")
    else:
        st.table(st.session_state.category_df)

    # カテゴリリストの削除
    if not st.session_state.category_df.empty:
        selected_category = st.selectbox("削除するカテゴリを選択:", st.session_state.category_df.Category, None)
        if st.button("カテゴリを削除"):
            st.session_state.category_df = st.session_state.category_df[
                st.session_state.category_df['Category'] != selected_category].reset_index(drop=True)
            st.success("タスクが削除されました!")
            # 再描画
            st.rerun()


def show_task_page():
    '''
    タスクの表示および編集と削除を行う
    データフレームを用いているためソートも可能
    '''
    # タスクの表示
    st.subheader("タスクリスト:")
    if st.session_state.tasks_df.empty:
        st.info("現在、タスクはありません。")
    else:
        st.write(st.session_state.tasks_df)

    # タスクの編集と削除
    if not st.session_state.tasks_df.empty:
        selected_task = st.selectbox("編集または削除するタスクを選択:", st.session_state.tasks_df.Task, None)
        # タスクがえらばたら編集と削除ができるようにする
        if selected_task:
            edited_task = st.text_input("編集後のタスクを入力してください:", value=selected_task)
            if st.button("タスク名を編集"):
                st.session_state.tasks_df.loc[st.session_state.tasks_df['Task'] == selected_task, 'Task'] = edited_task
                st.success("タスク名が編集されました!")
                # 再描画
                time.sleep(0.5)
                st.rerun()

            if st.button("タスクを削除"):
                st.session_state.tasks_df = st.session_state.tasks_df[
                    st.session_state.tasks_df['Task'] != selected_task].reset_index(drop=True)
                st.success("タスクが削除されました!")
                # 再描画
                time.sleep(0.5)
                st.rerun()

def show_about_page():
    st.title("このアプリについて")

def side_bar_choice():
    '''
    サイドバーでページ遷移およびタスクの入力を行う
    ここでタスクの追加を行う．
    '''
    def add_tasks(task, deadline, priority, category):
        # タスクをデータフレームに追加する
        new_task = pd.DataFrame({"Task": [task], "Deadline": [deadline], "Priority": [priority], "Category": [category]})
        st.session_state.tasks_df = pd.concat([st.session_state.tasks_df, new_task], ignore_index=True)
        st.success("タスクが追加されました!")

    # initialize
    task_input = input_meta_deadline = input_meta_priority = input_meta_category = None

    # 遷移ページの選択
    page = st.sidebar.selectbox("ページを選択してください", ["タスク管理", "カテゴリ", "使い方"])

    # タスクの入力
    with st.sidebar.form("input_task_form", clear_on_submit=True):
        # with st.sidebar:
        task_input = st.text_input("新しいタスクを入力してください:")
    
        # タスクに対するメタ情報
        if st.sidebar.checkbox("メタ情報を追加する"):
            input_meta_deadline = st.date_input("締切日", datetime.datetime.now())
            input_meta_priority = st.selectbox("優先度", list(range(1,6)))
            input_meta_category = st.selectbox("カテゴリ", st.session_state.category_df)
        
        st.form_submit_button("タスクを追加")

    # データフレームへタスクの追加を行う
    if task_input != "" and task_input != st.session_state.last_task :
        st.session_state.last_task = task_input
        add_tasks(task_input, input_meta_deadline, input_meta_priority, input_meta_category)

    return page

def main():
    st.title("タスクリスト")

    page = side_bar_choice()

    if page == "タスク管理":
        show_task_page()
    elif page == "カテゴリ":
        show_category_page()
    elif page == "使い方":
        show_about_page()

if __name__ == "__main__":
    main()
