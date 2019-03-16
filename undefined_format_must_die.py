#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import optuna
import subprocess

def format_file(path):
    if os.path.splitext(path)[1] in [".c", ".h", ".cpp", ".hpp"]:
        cmd = "clang-format-5.0 -i {}".format(path)
#        print(cmd)
        res = subprocess.run(cmd, shell=True)
    

def format_file_recursively(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            format_file_recursively(os.path.join(path,file))
    else:
        format_file(path)

def count_lines(res):
    tmp = res.stdout.decode("utf8")
    tmp = tmp.split(",")
    tmp.pop(0)
    res = 0
    for s in tmp:
        s=s.strip()
        s = s.split(" ")
        res += int(s[0])

    return res

def f(params):
    cmd_checkout      = "git checkout *"
    cmd_clean         = "git clean -fdx"
    cmd_create_conf   = "clang-format-5.0 -dump-config -style=\"{}\" > .clang-format".format(str(params))
    try:
        subprocess.run(cmd_checkout, shell=True)
        subprocess.run(cmd_clean,    shell=True)
#        print(cmd_create_conf)
        res = subprocess.run(cmd_create_conf, shell=True)

    except:
        print("Error")

    format_file_recursively(os.getcwd())
    cmd_count_diff = "git diff --shortstat"
    res = subprocess.run(cmd_count_diff, stdout=subprocess.PIPE, shell=True)

    return count_lines(res)


def objective(traial):

    params = {}
    params['IndentWidth']                               = traial.suggest_int('IndentWidth', 0, 8 )

    params['AccessModifierOffset']                      = traial.suggest_int('AccessModifierOffset', params['IndentWidth'], 16 )
    params['AlignAfterOpenBracket']                     = traial.suggest_categorical('AlignAfterOpenBracket', ['Align', 'DontAlign', 'AlwaysBreak'])
    params['AlignConsecutiveAssignments']               = traial.suggest_categorical('AlignConsecutiveAssignments', ['true', 'false'])
    params['AlignConsecutiveDeclarations']              = traial.suggest_categorical('AlignConsecutiveDeclarations', ['true', 'false'])
    params['AlignEscapedNewlinesLeft']                  = traial.suggest_categorical('AlignEscapedNewlinesLeft', ['true', 'false'])
    params['AlignOperands']                             = traial.suggest_categorical('AlignOperands', ['true', 'false'])
    params['AlignTrailingComments']                     = traial.suggest_categorical('AlignTrailingComments', ['true', 'false'])
    params['AllowAllParametersOfDeclarationOnNextLine'] = traial.suggest_categorical('AllowAllParametersOfDeclarationOnNextLine', ['true', 'false'])
    params['AllowShortBlocksOnASingleLine']             = traial.suggest_categorical('AllowShortBlocksOnASingleLine', ['true', 'false'])
    params['AllowShortCaseLabelsOnASingleLine']         = traial.suggest_categorical('AllowShortCaseLabelsOnASingleLine', ['true', 'false'])
    params['AllowShortFunctionsOnASingleLine']          = traial.suggest_categorical('AllowShortFunctionsOnASingleLine', ['None', 'Inline', 'Empty', 'All'])
    params['AllowShortIfStatementsOnASingleLine']       = traial.suggest_categorical('AllowShortIfStatementsOnASingleLine', ['true', 'false'])
    params['AllowShortLoopsOnASingleLine']              = traial.suggest_categorical('AllowShortLoopsOnASingleLine', ['true', 'false'])
    params['AlwaysBreakAfterReturnType']                = traial.suggest_categorical('AlwaysBreakAfterReturnType', ['None', 'All', 'TopLevel', 'AllDefinitions', 'TopLevelDefinitions'])
    params['AlwaysBreakBeforeMultilineStrings']         = traial.suggest_categorical('AlwaysBreakBeforeMultilineStrings', ['true', 'false'])
    params['AlwaysBreakTemplateDeclarations']           = traial.suggest_categorical('AlwaysBreakTemplateDeclarations', ['true', 'false'])
    params['BinPackArguments']                          = traial.suggest_categorical('BinPackArguments', ['true', 'false'])
    params['BinPackParameters']                         = traial.suggest_categorical('BinPackParameters', ['true', 'false'])

    params['BreakBeforeBraces']                         = traial.suggest_categorical('BreakBeforeBraces', ['Attach', 'Linux', 'Mozilla', 'Stroustrup', 'Allman', 'GNU', 'WebKit', 'Custom'])
    
    if params['BreakBeforeBraces'] == 'BS_Custom':
        params['BraceWrapping']['AfterClass']            = traial.suggest_categorical('AfterClass', ['true', 'false'])
        params['BraceWrapping']['AfterControlStatement'] = traial.suggest_categorical('AfterControlStatement', ['true', 'false'])
        params['BraceWrapping']['AfterEnum']             = traial.suggest_categorical('AfterEnum', ['true', 'false'])
        params['BraceWrapping']['AfterFunction']         = traial.suggest_categorical('AfterFunction', ['true', 'false'])
        params['BraceWrapping']['AfterNamespace']        = traial.suggest_categorical('AfterNamespace', ['true', 'false'])
        params['BraceWrapping']['AfterObjCDeclaration']  = traial.suggest_categorical('AfterObjCDeclaration', ['true', 'false'])
        params['BraceWrapping']['AfterStruct']           = traial.suggest_categorical('AfterStruct', ['true', 'false'])
        params['BraceWrapping']['AfterUnion']            = traial.suggest_categorical('AfterUnion', ['true', 'false'])
        params['BraceWrapping']['BeforeCatch']           = traial.suggest_categorical('BeforeCatch', ['true', 'false'])
        params['BraceWrapping']['BeforeElse']            = traial.suggest_categorical('BeforeElse', ['true', 'false'])
        params['BraceWrapping']['IndentBraces']          = traial.suggest_categorical('IndentBraces', ['true', 'false'])

    params['BreakBeforeBinaryOperators']                     = traial.suggest_categorical('BreakBeforeBinaryOperators', ['None', 'NonAssignment', 'All'])
    params['BreakBeforeTernaryOperators']                    = traial.suggest_categorical('BreakBeforeTernaryOperators', ['true', 'false'])
    params['BreakConstructorInitializersBeforeComma']        = traial.suggest_categorical('BreakConstructorInitializersBeforeComma', ['true', 'false'])
    params['BreakAfterJavaFieldAnnotations']                 = traial.suggest_categorical('BreakAfterJavaFieldAnnotations', ['true', 'false'])
    params['BreakStringLiterals']                            = traial.suggest_categorical('BreakStringLiterals', ['true', 'false'])
    params['ColumnLimit']                                    = traial.suggest_int('ColumnLimit', 0, 320)
    params['ConstructorInitializerAllOnOneLineOrOnePerLine'] = traial.suggest_categorical('ConstructorInitializerAllOnOneLineOrOnePerLine', ['true', 'false'])
    params['ConstructorInitializerIndentWidth']              = traial.suggest_int('ConstructorInitializerIndentWidth', 0, 16)
    params['ContinuationIndentWidth']                        = traial.suggest_int('ContinuationIndentWidth', 0, 16)
    params['Cpp11BracedListStyle']                           = traial.suggest_categorical('Cpp11BracedListStyle', ['true', 'false'])
    params['DerivePointerAlignment']                         = traial.suggest_categorical('DerivePointerAlignment', ['true', 'false'])
#    params['DisableFormat']                                  = traial.suggest_categorical('DisableFormat', ['true', 'false'])
    params['DisableFormat']                                  = traial.suggest_categorical('DisableFormat', ['false'])
    params['ExperimentalAutoDetectBinPacking']               = traial.suggest_categorical('ExperimentalAutoDetectBinPacking', ['true', 'false'])
    params['IndentCaseLabels']                               = traial.suggest_categorical('IndentCaseLabels', ['true', 'false'])
    params['IndentWrappedFunctionNames']                     = traial.suggest_categorical('IndentWrappedFunctionNames', ['true', 'false'])
    params['JavaScriptQuotes']                               = traial.suggest_categorical('JavaScriptQuotes', ['Leave', 'Single', 'Double'])
    params['JavaScriptWrapImports']                          = traial.suggest_categorical('JavaScriptWrapImports', ['true', 'false'])
    params['KeepEmptyLinesAtTheStartOfBlocks']               = traial.suggest_categorical('KeepEmptyLinesAtTheStartOfBlocks', ['true', 'false'])
    params['MaxEmptyLinesToKeep']                            = traial.suggest_int('MaxEmptyLinesToKeep', 0, 16)
    params['NamespaceIndentation']                           = traial.suggest_categorical('NamespaceIndentation', ['None', 'Inner', 'All'])
    params['ObjCBlockIndentWidth']                           = traial.suggest_int('ObjCBlockIndentWidth', 0, 16)
    params['ObjCSpaceAfterProperty']                         = traial.suggest_categorical('ObjCSpaceAfterProperty', ['true', 'false'])
    params['ObjCSpaceBeforeProtocolList']                    = traial.suggest_categorical('ObjCSpaceBeforeProtocolList', ['true', 'false'])
    params['PenaltyBreakBeforeFirstCallParameter']           = traial.suggest_int('PenaltyBreakBeforeFirstCallParameter', 0, 4294967295)
    params['PenaltyBreakComment']                            = traial.suggest_int('PenaltyBreakComment', 0, 4294967295)
    params['PenaltyBreakFirstLessLess']                      = traial.suggest_int('PenaltyBreakFirstLessLess', 0, 4294967295)
    params['PenaltyBreakString']                             = traial.suggest_int('PenaltyBreakString', 0, 4294967295)
    params['PenaltyExcessCharacter']                         = traial.suggest_int('PenaltyExcessCharacter', 0, 4294967295)
    params['PenaltyReturnTypeOnItsOwnLine']                  = traial.suggest_int('PenaltyReturnTypeOnItsOwnLine', 0, 4294967295)
    params['PointerAlignment']                               = traial.suggest_categorical('PointerAlignment', ['Left', 'Right', 'Middle'])
    params['ReflowComments']                                 = traial.suggest_categorical('ReflowComments', ['true', 'false'])
    params['SortIncludes']                                   = traial.suggest_categorical('SortIncludes', ['true', 'false'])
    params['SpaceAfterCStyleCast']                           = traial.suggest_categorical('SpaceAfterCStyleCast', ['true', 'false'])
    params['SpaceBeforeAssignmentOperators']                 = traial.suggest_categorical('SpaceBeforeAssignmentOperators', ['true', 'false'])
    params['SpaceBeforeParens']                              = traial.suggest_categorical('SpaceBeforeParens', ['Never', 'ControlStatements', 'Always'])
    params['SpaceInEmptyParentheses']                        = traial.suggest_categorical('SpaceInEmptyParentheses', ['true', 'false'])
    params['SpacesBeforeTrailingComments']                   = traial.suggest_int('SpacesBeforeTrailingComments', 0, 8)
    params['SpacesInAngles']                                 = traial.suggest_categorical('SpacesInAngles', ['true', 'false'])
    params['SpacesInContainerLiterals']                      = traial.suggest_categorical('SpacesInContainerLiterals', ['true', 'false'])
    params['SpacesInCStyleCastParentheses']                  = traial.suggest_categorical('SpacesInCStyleCastParentheses', ['true', 'false'])
    params['SpacesInParentheses']                            = traial.suggest_categorical('SpacesInParentheses', ['true', 'false'])
    params['SpacesInSquareBrackets']                         = traial.suggest_categorical('SpacesInSquareBrackets', ['true', 'false'])
    params['Standard']                                       = traial.suggest_categorical('Standard', ['Cpp03', 'Cpp11', 'Auto'])
    params['TabWidth']                                       = traial.suggest_int('TabWidth', 1, 64 )
    params['UseTab']                                         = traial.suggest_categorical('UseTab', ['Never', 'ForIndentation', 'Always'])

    return f(params)

#    x = traial.suggest_uniform('x', -5, +15)
#    return - math.exp(-(x-2) ** 2) + math.exp(-(x-6) ** 2/10) + 1 / (x ** 2 + 1)



def main():
    study = optuna.create_study()
    study.optimize(objective, n_trials=1000)
    print('params:', study.best_params)

if __name__ == '__main__':
    main()
