class Script:
    def execute(self, data):
        gcode_to_add = "test" + "\n"

        for layer in data:
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";Generated with Cura"):
                    line_index = lines.index(line)
                    lines[line_index] = gcode_to_add + line
                    break

            final_lines = "\n".join(lines)
            data[layer_index] = final_lines

        return data