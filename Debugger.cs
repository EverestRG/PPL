using System;
using System.IO;

namespace Compiler
{
    internal class Debugger
    {
        public bool Debug(string pplfile)
        {
            string filetext = File.ReadAllText(pplfile);
            string[] spearator = { Environment.NewLine, "\n" };
            string[] strlist = filetext.Split(spearator, StringSplitOptions.RemoveEmptyEntries);
            for (int i = 0; i < strlist.Length; i++)
            {
                try
                {
                    if (strlist[i].Contains("$")) { Console.WriteLine($"EXCEPTION:\n  Forbidden character '$' at line: {i.ToString()}\n    >>{strlist[i]}"); return false; }
                    if (!strlist[i].Replace(" ", "").EndsWith(";") && !strlist[i].Replace(" ", "").EndsWith("}") && !strlist[i].Replace(" ", "").EndsWith("{")) { if (!strlist[i + 1].Replace(" ", "").StartsWith("{")) { Console.WriteLine($"EXCEPTION:\n  Expected ';' at line: {i.ToString()}\n    >>{strlist[i]}"); return false; } }
                    if (strlist[i].Contains("import"))
                    {
                        string[] lists = filetext.Split(' ');
                        int TextIndex = Array.FindIndex(lists, m => m == "import");
                        try
                        {
                            if (lists[TextIndex + 2] != "as")
                            {
                                Console.WriteLine($"EXCEPTION:\n  Expected 'as' at line: {i.ToString()}\n    >>{strlist[i]}");
                                return false;
                            }
                        }
                        catch
                        {
                            Console.WriteLine($"EXCEPTION:\n  Expected 'as' at line: {i.ToString()}\n    >>{strlist[i]}");
                            return false;
                        }
                        string curpth = Directory.GetCurrentDirectory() + "\\" + Path.GetFileName(pplfile);
                        string importfs = curpth.Replace(Path.GetFileName(pplfile), "") + $"\\{lists[TextIndex+1]}.ppl";
                        try
                        {
                            File.ReadAllText(importfs);
                        }
                        catch
                        {
                            Console.WriteLine($"EXCEPTION:\n  Unknown module name '{lists[TextIndex+1]}' at line: {i.ToString()}\n    >>{strlist[i]}");
                            return false;
                        }
                    }
                }
                catch
                {
                    continue;
                }
            }
            return true;
        }
    }
}
