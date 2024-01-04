from pisa_client import initialise_env


if __name__ == '__main__':
    env = initialise_env()
    default_st = env.initialise()
    
    # Default state
    print(default_st)

    # Returns error string!
    # obs_string = env.step('default', 'theory Drinker', 'state0', delete_old_state=False)
    # print(obs_string)

    # Initialization of theory
    obs_string = env.step('default', 'theory Drinker imports Main begin', 'state0', delete_old_state=False)
    print(obs_string)

    # Declare a lemma
    obs_string = env.step('state0', 
                          'lemma de_Morgan: assumes "\\<not> (\\<forall>x. P x)" shows "\\<exists>x. \\<not> P x"',
                          'state1', 
                          delete_old_state=False)
    print(env.get_state('state1'))

    all_lemmas = env.get_total_lemmas('state1')
    print("Num lemmas: " + str(len(all_lemmas)))
    print(all_lemmas[0:10]) # First 10 lemmas
    for lemma in all_lemmas: # Sanity check with less complicated/weird lemmas
        if "ln_gt_zero" in lemma:
            print(lemma)

    # Attempt to use Sledgehammer
    obs_string = env.apply_hammer('state1', 'hammered')
    print(obs_string)
    print("Finished? " + str(env.is_finished('hammered')))

    # Prove the lemma
    obs_string = env.step('state1', 
                          "proof (rule classical)",
                          'state2', 
                          delete_old_state=False)
    print(obs_string)
    obs_string = env.step('state2', 
                          "assume \"\\<nexists>x. \\<not> P x\"",
                          'state3', 
                          delete_old_state=False)
    print(obs_string)
    obs_string = env.step('state3', 
                          """
have "\\<forall>x. P x"
proof
fix x show "P x"
proof (rule classical)
    assume "\\<not> P x"
    then have "\\<exists>x. \\<not> P x" ..
    with \\<open>\\<nexists>x. \\<not> P x\\<close> show ?thesis by contradiction
qed
qed
                          """,
                          'state4', 
                          delete_old_state=False)
    print(obs_string)
    obs_string = env.step('state4', 
                          "with \\<open>\\<not> (\\<forall>x. P x)\\<close> show ?thesis by contradiction",
                          'state5', 
                          delete_old_state=False)
    print(obs_string)

    # Proof is not done until qed
    print("Finished? " + str(env.is_finished('state5')))
    obs_string = env.step('state5', 
                          'qed',
                          'state6', 
                          delete_old_state=False)
    print("Finished? " + str(env.is_finished('state6')))

