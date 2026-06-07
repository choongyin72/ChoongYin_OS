*** Settings ***
Documentation       T1 (universal) aggregator — imports every shared EC keyword area
...                 so a suite can import this one file for everything, or cherry-pick
...                 an individual area file (browser / screen / toolbar / table / utils).

Resource            browser.resource
Resource            screen.resource
Resource            toolbar.resource
Resource            table.resource
Resource            utils.resource
Variables           environment.py
