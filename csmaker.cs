using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;

namespace Compiler
{
    internal class csmaker
    {
        public void BuildCS(string pplfile, string name, bool ismain)
        {
            Console.WriteLine($"Building {pplfile.Split('.')[pplfile.Split('.').Length - 2]}.cs...");
            csprojMaker maker = new csprojMaker();
            string filetext = File.ReadAllText(pplfile);
            List<string> usings = new List<string>();
            if (ismain)
            {
                filetext = "static void Main(string[] args) {" + Environment.NewLine + filetext + Environment.NewLine + "}";
            }
            filetext = "internal class " + Path.GetFileNameWithoutExtension(pplfile) + " {" + Environment.NewLine + filetext + Environment.NewLine + "}";
            filetext = "namespace " + Path.GetFileNameWithoutExtension(name) + " {" + Environment.NewLine + filetext + Environment.NewLine + "}";
            if (filetext.ToLower().Contains("print(") || filetext.ToLower().Contains("println(") || filetext.ToLower().Contains("read(") || filetext.ToLower().Contains("readln("))
            {
                usings.Add("System");
            }
            if (filetext.ToLower().Contains("file.") || filetext.ToLower().Contains("path."))
            {
                usings.Add("System.IO");
            }
            if (filetext.ToLower().Contains("list<"))
            {
                usings.Add("System.Collections.Generic");
            }
            if (filetext.ToLower().Contains("messagebox."))
            {
                usings.Add("System.Windows.Forms");
            }
            for (int i = 0; i < usings.Count; i++)
            {
                filetext = "using " + usings[i] + ";" + Environment.NewLine + filetext;
            }
            filetext = filetext.Replace("Please ", "");
            filetext = filetext.Replace("Thanks", "");
            filetext = filetext.Replace("println(", "Console.WriteLine(");
            filetext = filetext.Replace("readln(", "Console.ReadLine(");
            filetext = filetext.Replace("print(", "Console.Write(");
            filetext = filetext.Replace("read(", "Console.Read(");
            string imports = "nn";
            while (imports != "")
            {
                imports = maker.getBetween(filetext, "import ", " as");
                string asses = maker.getBetween(filetext, " as ", ";");
                filetext = filetext.Replace($"import {imports} as {asses};", $"{imports} {asses} = new {imports}();");
            }
            File.WriteAllText(pplfile.Split('.')[pplfile.Split('.').Length - 2] + ".cs", $@"{filetext}", encoding: System.Text.Encoding.UTF8);
            Console.WriteLine($"Built {pplfile.Split('.')[pplfile.Split('.').Length - 2]}.cs");
        }
    }
}
