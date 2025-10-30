# import subprocess
#
# def dot_to_png(dot_filename, png_filename="output.png"):
#     try:
#         subprocess.run(['dot', '-Tpng', dot_filename, '-o', png_filename], check=True)
#         print(f"PNG file generated: {png_filename}")
#     except subprocess.CalledProcessError as e:
#         print("Error generating PNG:", e)

import subprocess
import os



def dot_to_png(dot_filename, png_filename="output.png"):
    if not os.path.isfile(dot_filename):
        print(f"DOT file not found: {dot_filename}")
        return
    try:
        subprocess.run(['dot', '-Tpng', dot_filename, '-o', png_filename], check=True)
        print(f"PNG file generated: {png_filename}")
    except subprocess.CalledProcessError as e:
        print("Error generating PNG:", e)

#usage example
if __name__ == "__main__":
    dot_to_png("../result_coffeemachine/BiasedSAT/coffeemachine_0_50_BiasedSAT.dot",
               "../result_coffeemachine/BiasedSAT/coffeemachine_0_50_BiasedSAT.png")
    dot_to_png("../result_coffeemachine/BiasedSATPAT/coffeemachine_0_50_BiasedSATPAT.dot",
               "../result_coffeemachine/BiasedSATPAT/coffeemachine_0_50_BiasedSATPAT.png")