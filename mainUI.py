import tkinter
from tkinter import filedialog, ttk, messagebox, Frame
from Crypto.PublicKey import RSA
from PIL import Image, ImageDraw, ImageTk
from DigitalSignatures import RSASign, RSAVerify
from ReadFileDocx import read_docx
import os

check = None
signature = None

def BrowseFileBtnClicked(file_entry: tkinter.Entry) -> None:
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tkinter.END)
        file_entry.insert(0, file_path)

def SignBtnClicked(root_file_entry: tkinter.Entry, private_entry: tkinter.Entry) -> None:
    root_url = root_file_entry.get()
    private_url = private_entry.get()
    try:
        if root_url.endswith(".docx"):
            data = read_docx(root_url)
        else:
            with open(root_url, encoding="utf-8") as f:
                data = f.read()
        with open(private_url, "rb") as f:
            private_key = RSA.import_key(f.read())

        global signature
        signature = RSASign(data, private_key)
        sign_file_name = os.path.basename(root_url) + ".sig"
        with open(sign_file_name, "wb") as f:
            f.write(signature)
        messagebox.showinfo("Thành công", "Kí thành công")
    except TypeError:
        messagebox.showerror("Lỗi", f"Key được chọn phải là private key")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", f"Không tìm thấy file")

def VerifyBtnClicked(check_file_entry: tkinter.Entry, sign_file_entry: tkinter.Entry, public_key_entry: tkinter.Entry) -> None:
    check_url = check_file_entry.get()
    sign_url = sign_file_entry.get()
    public_url = public_key_entry.get()
    try:
        if check_url.endswith(".docx"):
            data = read_docx(check_url)
        else:
            with open(check_url, encoding="utf-8") as f:
                data = f.read()
        with open(public_url, "rb") as f:
            public_key = RSA.import_key(f.read())
        with open(sign_url, "rb") as f:
            signature = f.read()
        if public_key.has_private():
            messagebox.showerror("Lỗi", "Key được chọn phải là public key")
            return
        
        global check
        check = RSAVerify(data, signature, public_key)
        if check:
            messagebox.showinfo("Thành công", "Chữ ký hợp lệ\nVăn bản chính xác")
        else:
            messagebox.showerror("Thất bại", "Chữ ký không hợp lệ\nVăn bản đã bị chỉnh sửa")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", f"Không thể đọc file")

def GenKeyBtnClicked() -> None:
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    with open("private_key.pem", "wb") as f:
        f.write(private_key.export_key())
    with open("public_key.pem", "wb") as f:
        f.write(public_key.export_key())
    messagebox.showinfo("Thành công", "Tạo khóa thành công")

def SignScr(master: Frame):
    tkinter.Label(master, text="Chọn File cần kí", width=15).grid(column=0, row=0, padx=5, pady=5)
    root_file_entry = tkinter.Entry(master, width=45)
    root_file_entry.grid(column=1, row=0, padx=5, pady=5)
    root_button = create_button_with_rounded_corners(master, "Chọn file", lambda: BrowseFileBtnClicked(root_file_entry), 100, 30, 10, '#4CAF50')
    root_button.grid(column=2, row=0, padx=5, pady=5)

    tkinter.Label(master, text="Chọn File private key", width=15).grid(column=0, row=1, padx=5, pady=5)
    private_key_entry = tkinter.Entry(master, width=45)
    private_key_entry.grid(column=1, row=1, padx=5, pady=5)
    private_key_button = create_button_with_rounded_corners(master, "Chọn file", lambda: BrowseFileBtnClicked(private_key_entry), 100, 30, 10, '#4CAF50')
    private_key_button.grid(column=2, row=1, padx=5, pady=5)

    sign_button = create_button_with_rounded_corners(master, "Kí", lambda: SignBtnClicked(root_file_entry, private_key_entry), 200, 40, 10, '#2196F3')
    sign_button.grid(column=1, row=2, padx=5, pady=10)

def VerifyScr(master: Frame):
    tkinter.Label(master, text="Chọn File kiểm tra", width=15).grid(column=0, row=0, padx=5, pady=5)
    check_file_entry = tkinter.Entry(master, width=45)
    check_file_entry.grid(column=1, row=0, padx=5, pady=5)
    check_button = create_button_with_rounded_corners(master, "Chọn file", lambda: BrowseFileBtnClicked(check_file_entry), 100, 30, 10, '#4CAF50')
    check_button.grid(column=2, row=0, padx=5, pady=5)
    
    tkinter.Label(master, text="Chọn File public key", width=15).grid(column=0, row=1, padx=5, pady=5)
    public_key_entry = tkinter.Entry(master, width=45)
    public_key_entry.grid(column=1, row=1, padx=5, pady=5)
    public_key_button = create_button_with_rounded_corners(master, "Chọn file", lambda: BrowseFileBtnClicked(public_key_entry), 100, 30, 10, '#4CAF50')
    public_key_button.grid(column=2, row=1, padx=5, pady=5)

    tkinter.Label(master, text="Chọn File chữ kí", width=15).grid(column=0, row=2, padx=5, pady=5)
    sign_file_entry = tkinter.Entry(master, width=45)
    sign_file_entry.grid(column=1, row=2, padx=5, pady=5)
    sign_button = create_button_with_rounded_corners(master, "Chọn file", lambda: BrowseFileBtnClicked(sign_file_entry), 100, 30, 10, '#4CAF50')
    sign_button.grid(column=2, row=2, padx=5, pady=5)
    
    verify_button = create_button_with_rounded_corners(master, "Kiểm tra", lambda: VerifyBtnClicked(check_file_entry, sign_file_entry, public_key_entry), 200, 40, 10, '#2196F3')
    verify_button.grid(column=1, row=3, padx=5, pady=10)

def GenKeySrc(master: Frame) -> None:
    gen_key_button = create_button_with_rounded_corners(master, "Tạo khóa", GenKeyBtnClicked, 200, 40, 10, '#2196F3')
    gen_key_button.pack()

def create_rounded_rectangle_image(width, height, radius, color):
    image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return ImageTk.PhotoImage(image)

def create_button_with_rounded_corners(master, text, command, width, height, radius, bg_color):
    image = create_rounded_rectangle_image(width, height, radius, bg_color)
    button = tkinter.Button(master, text=text, command=command, image=image, compound="center", fg='white', font=('Arial', 10, 'bold'), borderwidth=0, highlightthickness=0)
    button.image = image  # keep a reference to prevent garbage collection
    return button

def main():
    root = tkinter.Tk()
    root.title("Digital Signature Application")
    root.geometry("600x400")
    root.resizable(False, False)
    root.configure(bg="lightblue")

    container_frame = Frame(root, bg="lightblue", padx=10, pady=10)
    container_frame.grid(column=0, row=0, padx=10, pady=10)
    
    tab_control = ttk.Notebook(container_frame)
    tab_sign = ttk.Frame(tab_control, padding=10)
    tab_veri = ttk.Frame(tab_control, padding=10)
    tab_gen_key = ttk.Frame(tab_control, padding=10)

    tab_control.add(tab_sign, text="Signature")
    tab_control.add(tab_veri, text="Verify")
    tab_control.add(tab_gen_key, text="Generate Key")
    tab_control.grid(column=0, row=0, padx=10, pady=10)

    SignScr(tab_sign)
    VerifyScr(tab_veri)
    GenKeySrc(tab_gen_key)

    root.mainloop()
    
if __name__ == "__main__":
    main()