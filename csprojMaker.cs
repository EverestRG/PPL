using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Resources;

namespace Compiler
{
    internal class csprojMaker
    {
        public string getBetween(string strSource, string strStart, string strEnd)
        {
            if (strSource.Contains(strStart) && strSource.Contains(strEnd))
            {
                int Start, End;
                Start = strSource.IndexOf(strStart, 0) + strStart.Length;
                End = strSource.IndexOf(strEnd, Start);
                return strSource.Substring(Start, End - Start);
            }

            return "";
        }
        public void MakeProj(string path, List<string> csfiles, string icon = "")
        {
            Console.WriteLine("Building .csproj...");
            string filetext = File.ReadAllText($"{Path.GetDirectoryName(Assembly.GetEntryAssembly().Location)}\\csproj.cmp");
            List<string> usings = new List<string>();
            string nmspc = "";
            for (int i = 0; i < csfiles.Count; i++)
            {
                string temptext = File.ReadAllText(csfiles[i]);
                if (temptext.ToLower().Contains("console.") && !usings.Contains("System"))
                {
                    usings.Add("System");
                }
                if ((temptext.ToLower().Contains("file.") || temptext.ToLower().Contains("path.")) && !usings.Contains("System.IO"))
                {
                    usings.Add("System.IO");
                }
                if (temptext.ToLower().Contains("list<") && !usings.Contains("System.Collections.Generic"))
                {
                    usings.Add("System.Collections.Generic");
                }
                if (temptext.ToLower().Contains("messagebox.") && !usings.Contains("System.Windows.Forms"))
                {
                    usings.Add("System.Windows.Forms");
                }
                nmspc = getBetween(temptext, "namespace ", " {");
            }
            for (int i = 0;i < usings.Count;i++)
            {
                string oldext = filetext;
                filetext = filetext.Replace("    %USINGS%", "    <Reference Include=\"" + usings[i] + "\" />");
                if (oldext == filetext)
                {
                    filetext = filetext.Replace("    <Reference Include=\"" + usings[i-1] + "\" />", "    <Reference Include=\"" + usings[i-1] + "\" />" + Environment.NewLine + "    <Reference Include=\"" + usings[i] + "\" />");
                }
            }
            for (int i = 0; i < csfiles.Count; i++)
            {
                string oldext = filetext;
                filetext = filetext.Replace("%CSFILES%", "<Compile Include=\"" + Path.GetFileName(csfiles[i]) + "\" />");
                if (oldext == filetext)
                {
                    filetext = filetext.Replace("<Compile Include=\"" + Path.GetFileName(csfiles[i-1]) + "\" />", "<Compile Include=\"" + Path.GetFileName(csfiles[i-1]) + "\" />" + Environment.NewLine + "    <Compile Include=\"" + Path.GetFileName(csfiles[i]) + "\" />");
                }
            }
            filetext = filetext.Replace("%NAME%", nmspc);
            if (icon != "")
            {
                filetext = filetext.Replace("%ICONPATH%", icon);
            }
            else
            {
                filetext = filetext.Replace("\n    <ApplicationIcon>%ICONPATH%</ApplicationIcon>", "");
            }
            FileInfo fi = new FileInfo(path);
            File.WriteAllText(fi.DirectoryName + "\\" + nmspc + ".csproj", $"{filetext}", encoding: System.Text.Encoding.UTF8);
            Console.WriteLine("Built .csproj successfully!");
        }
    }
}
