from PIL import Image
import os


def cut_image(image_path, output_folder, rows, cols):
    # Open the image file
    image = Image.open(image_path)
    img_width, img_height = image.size

    # Calculate the size of each piece
    piece_width = img_width // cols
    piece_height = img_height // rows

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for i in range(rows):
        for j in range(cols):
            # Calculate the coordinates of the piece
            left = j * piece_width
            upper = i * piece_height
            right = (j + 1) * piece_width
            lower = (i + 1) * piece_height

            # Crop the piece from the image
            piece = image.crop((left, upper, right, lower))

            # Save the piece to a file
            piece_path = os.path.join(output_folder, f"card{i}{j+1}.png")
            piece.save(piece_path)
            print(f"Saved piece {i},{j+1} to {piece_path}")


#function used to cut collective images af cards and card backs into single pictures
cut_image("graphics/cardBacks.png", "graphics/backs", 4, 13)
cut_image("graphics/cardBacks.png", "graphics/backs", 2, 2)
