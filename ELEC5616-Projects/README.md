# ELEC5616-Projects

## About the Repository
This code in this repository is for the ELEC5616 Computer and Network Security subject at the University of Sydney.

## Getting Started
1. Log into git and view the ELEC5615-Projects repo
2. For the HTTPS link, in your terminal, type `git clone "URL"`

If you are making any changes, do the following, for further info plz check [Link](http://product.hubspot.com/blog/git-and-github-tutorial-for-beginners)
1. `git add .`
2. `git commit -m "brief description of changes"`
3. `git push`
4. **ALWAYS COMMENT COMMITS**

Before you start making **any** changes, do the following
1. `git pull`
2. Post in the slack, what you are working on and which files you plan on changing

## Pushing code to phab
The first way is:
1. cd to ELEC5615-Projects folder
2. `git remote add phab https://phab.elec5616.com/diffusion/SIX/skynetproject.git`
3. Then, you can push your code to phab directly by `git push phab <branch>`

The second way is:
1. cd to a empty folder/desktop/anywhere
2. `git clone https://phab.elec5616.com/diffusion/SIX/skynetproject.git`
3. Then, you can push your code as normal git usage
