using System;
using System.Windows.Forms;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;

namespace Compiler
{
    internal class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                bool keyp = true;
                string[] lastIndex = Path.GetFileName(args[0]).Split('.');
                ConsoleKeyInfo cki;
                if (lastIndex[lastIndex.Length-1].ToLower() == "ppl")
                {
                    bool cmpinterrupt = true;
                    csprojMaker maker = new csprojMaker();
                    csmaker csmaker = new csmaker();
                    string filetext = "";
                    string curpth = "";
                    if (args[0].Replace(Path.GetFileName(args[0]), "") != "")
                    {
                        filetext = File.ReadAllText(args[0]);
                        curpth = args[0];
                    }
                    else
                    {
                        filetext = File.ReadAllText(Directory.GetCurrentDirectory() + "\\" + args[0]);
                        curpth = Directory.GetCurrentDirectory() + "\\" + args[0];
                    }
                    string newfile = $"{lastIndex[lastIndex.Length - 2]}";
                    Console.WriteLine($"Working with: {newfile}.ppl");
                    List<string> csfiles = new List<string>();
                    void comp(string cmdd)
                    {
                        Process cmd = new Process();
                        cmd.StartInfo.FileName = "cmd.exe";
                        cmd.StartInfo.RedirectStandardInput = true;
                        cmd.StartInfo.RedirectStandardOutput = true;
                        cmd.StartInfo.CreateNoWindow = true;
                        cmd.StartInfo.UseShellExecute = false;
                        cmd.Start();
                        cmd.StandardInput.WriteLine(cmdd);
                        cmd.StandardInput.Flush();
                        cmd.StandardInput.Close();
                        cmd.WaitForExit();
                        Console.WriteLine(cmd.StandardOutput.ReadToEnd());
                    }
                    try
                    {
                        Console.WriteLine($"Naming exe as {Path.GetFileNameWithoutExtension(args[1])}");
                        bool compiling = true;
                        if (csmaker.BuildCS(args[0], Path.GetFileNameWithoutExtension(args[1]), true)) { } else { compiling = false; }
                        csfiles.Add(args[0].Replace(".ppl", ".cs"));
                        string imports = "nn";
                        while (imports != "")
                        {
                            imports = maker.getBetween(filetext, "import ", " as");
                            if (imports == "") { break; }
                            if (compiling) { if (csmaker.BuildCS(curpth.Replace(Path.GetFileName(curpth), "") + imports + ".ppl", args[1], false)) { } else { compiling = false; } }
                            csfiles.Add(curpth.Replace(Path.GetFileName(curpth), "") + imports + ".cs");
                            filetext = filetext.Replace($"import {imports} as", "");
                        }
                        try
                        {
                            if (compiling) { maker.MakeProj(args[0], csfiles, args[3]); }
                        }
                        catch
                        {
                            if (compiling) { maker.MakeProj(args[0], csfiles); }
                        }
                        FileInfo fi = new FileInfo(args[0]);
                        string Full = fi.DirectoryName + "\\" + Path.GetFileNameWithoutExtension(args[1]) + ".csproj";
                        string cmd = $"\"C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe\" \"{Full}\"";
                        if (compiling) { comp(cmd); } else { Console.WriteLine("Compilation unsuccessfull"); cmpinterrupt = false; }
                    }
                    catch
                    {
                        Console.WriteLine($"Naming exe as {newfile}");
                        bool compiling = true;
                        if (csmaker.BuildCS(args[0], newfile, true)) { } else { compiling = false; }
                        csfiles.Add(curpth.Replace(Path.GetFileName(curpth), "") + newfile + ".cs");
                        string imports = "nn";
                        while (imports != "")
                        {
                            imports = maker.getBetween(filetext, "import ", " as");
                            if (imports == "") { break; }
                            if (compiling) { if (csmaker.BuildCS(curpth.Replace(Path.GetFileName(curpth), "") + imports + ".ppl", newfile, false)) { } else { compiling = false; } }
                            csfiles.Add(curpth.Replace(Path.GetFileName(curpth), "") + imports + ".cs");
                            filetext = filetext.Replace($"import {imports} as", "");
                        }
                        if (compiling) { maker.MakeProj(args[0], csfiles); }
                        FileInfo fi = new FileInfo(args[0]);
                        string Full = fi.DirectoryName + "\\" + newfile + ".csproj";
                        string cmd = $"\"C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe\" \"{Full}\"";
                        if (compiling) { comp(cmd); } else { Console.WriteLine("Compilation interrupted"); cmpinterrupt = false; }
                    }
                    try
                    {
                        if (args[2].ToLower() != "true")
                        {
                            Directory.Delete(curpth.Replace(Path.GetFileName(curpth), "") + "\\obj", true);
                            File.Delete(curpth.Replace(Path.GetFileName(curpth), "") + args[1] + ".csproj");
                            for (int i = 0; i < csfiles.Count; i++)
                            {
                                File.Delete(csfiles[i]);
                            }
                        }
                        if (!File.Exists(curpth.Replace(Path.GetFileName(curpth), "") + "\\bin\\" + args[1] + ".exe")) { cmpinterrupt = false; }
                    }
                    catch
                    {
                        try
                        {
                            Directory.Delete(curpth.Replace(Path.GetFileName(curpth), "") + "\\obj", true);
                            File.Delete(curpth.Replace(Path.GetFileName(curpth), "") + args[1] + ".csproj");
                            if (!File.Exists(curpth.Replace(Path.GetFileName(curpth), "") + "\\bin\\" + args[1] + ".exe")) {  cmpinterrupt = false; }
                        }
                        catch
                        {
                            Directory.Delete(curpth.Replace(Path.GetFileName(curpth), "") + "\\obj", true);
                            File.Delete(curpth.Replace(Path.GetFileName(curpth), "") + newfile + ".csproj");
                            if (!File.Exists(curpth.Replace(Path.GetFileName(curpth), "") + "\\bin\\" + newfile + ".exe")) { cmpinterrupt = false; }
                        }
                        for (int i = 0; i < csfiles.Count; i++)
                        {
                            File.Delete(csfiles[i]);
                        }
                    }
                    if (cmpinterrupt) { Console.WriteLine("Compilation done!"); }
                    else
                    {
                        Console.WriteLine("Press any key to close");
                        while (keyp)
                        {
                            cki = Console.ReadKey();
                            if (cki.Equals(cki))
                            {
                                keyp = false;
                            }
                        }
                    }
                }
                else
                {
                    MessageBox.Show("This file extension can not be compiled via PPL compiler.", "Compiler error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    Environment.Exit(0);
                }
            }
            else
            {
                MessageBox.Show("You must run a *.ppl file via this compiler", "Compiler error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Environment.Exit(0);
            }
        }
    }
}