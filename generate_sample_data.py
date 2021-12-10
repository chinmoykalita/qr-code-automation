from PIL import ImageDraw, ImageFont
import os
import qrcode


def group_photos(clients: int):
    """Renames photos into groups depending on the total number of clients.
    This makes it possible to assign a qr code to each group of photos

    Args:
        clients (int): Total number of clients
    """
    files = [
        f
        for f in sorted(os.listdir("sample_data"))
        if f.endswith("jpg")
        or f.endswith("png")
        or f.endswith("jpeg")
        or f.endswith("JPG")
    ]
    group_size = len(files) // clients
    # distribute photos to all events equally
    groups = [files[group_size * i : group_size * (i + 1)] for i in range(clients)]
    remainders = len(files) % clients
    # if anything remains, add to the last event
    if remainders > 0:
        [groups[-1].append(i) for i in files[-remainders:]]

    for group_number, group in enumerate(groups, start=1):
        for count, f in enumerate(group, start=1):
            os.rename(
                f"sample_data/{f}",
                f"sample_data/IMG_{group_number}00{count}.{f.split('.')[-1]}",
            )


def convert_image_names():
    """convert all images including qr codes names to simulate naming scheme from a camera"""
    files = [f for f in sorted(os.listdir("sample_data"))]
    for i, f in enumerate(files, start=1):
        os.rename(f"sample_data/{f}", f"sample_data/IMG_{i:003}.{f.split('.')[-1]}")


def rename_qr_codes():
    """Give the qr codes a name that places them right above the group they represent.
    This simulates the photographer taking a photo of the qr code before a shoot starts.
    This should be run only at the after the photos have been grouped.
    """
    files = [f for f in sorted(os.listdir("sample_data")) if "IMG" not in f]
    for position, f in enumerate(files, start=1):
        os.rename(
            f"sample_data/{f}", f"sample_data/IMG_{position}000.{f.split('.')[-1]}"
        )


def add_text(payload: str, qr):
    font = ImageFont.truetype("ArundinaSans.ttf", 30)
    img = ImageDraw.Draw(qr)
    width, height = qr.size
    img.text((width // 3, height - 45), payload, font=font)
    return qr


def generate_qr(payload: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=3,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    file_name = os.path.join(f"sample_data/{payload}.png")
    add_text(payload, img).save(file_name)
    return img


if __name__ == "__main__":
    events = ["0912212", "1012214"]
    clients_per_shoot = 2
    shoots = [f"{e}{n:02}" for e in events for n in range(1, clients_per_shoot + 1)]
    group_photos(len(events) * clients_per_shoot)
    for shoot in shoots:
        generate_qr(shoot)
    rename_qr_codes()
    convert_image_names()
