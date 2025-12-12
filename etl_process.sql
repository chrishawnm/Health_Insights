used the following website to format the sql script: https://www.dpriver.com/pp/sqlformat.htm

— this table is essentially getting the joined table with sex, race and county mapping
		     CREATE OR replace TABLE `cs-6440.bfs.sample_data_labels` AS
                        WITH locale                      AS
                        (
                               SELECT state_ssa_code,
                                      cast(RIGHT(cast(state_county_ssa_code AS string), 3) AS int64) AS county_id,
                                      state_                                                         AS state_name,
                                      state_county                                                   AS county_name
                               FROM   `cs-6440.bfs.state_county_mapping_internal`
                        )SELECT    a.desynpuf_id,
                           a.bene_birth_dt,
                           a.bene_death_dt,
                           a.bene_sex_ident_cd,
                           a.bene_race_cd,
                           a.bene_esrd_ind,
                           a.sp_state_code,
                           a.bene_county_cd,
                           a.sp_alzhdmta,
                           a.sp_chf,
                           a.sp_chrnkidn,
                           a.sp_cncr,
                           a.sp_copd,
                           a.sp_depressn,
                           a.sp_diabetes,
                           a.sp_ischmcht,
                           a.sp_osteoprs,
                           a.sp_ra_oa,
                           a.sp_strketia,
                           loc.state_name,
                           loc.county_name,
                           race.label                                                                           AS race,
                           sex.label                                                                            AS sex_label,
                           Parse_date('%Y%m%d', Cast(bene_birth_dt AS STRING))                                  AS birth_date,
                           Date_diff(CURRENT_DATE(), Parse_date('%Y%m%d', Cast(bene_birth_dt AS STRING)), year) AS age
                 FROM      `cs-6440.bfs.sample_data_combined_internal` a
                 LEFT JOIN locale loc
                 ON        a.sp_state_code = loc.state_ssa_code
                 AND       a.bene_county_cd = loc.county_id
                 LEFT JOIN `cs-6440.bfs.race_table_mapping_internal` race
                 ON        a.bene_race_cd = race.code
                 LEFT JOIN `cs-6440.bfs.sex_table_mapping_internal` sex
                 ON        a.bene_sex_ident_cd = sex.code;

—- this IS the dataset weUSE for the FILE data2.csv
— this table is essentially creating a table that is aggregating all county,state, race,sex and getting the count of how many people and avg_age of them
                 CREATE OR replace TABLE `cs-6440.bfs.sample_data_agg` ASSELECT   'Alzheimer'  AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          Cast(Avg(age) AS INT) AS avg_age,
                          Count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_alzhdmta = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Heart Failure' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_chf = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Chronic Kidney Disease' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_chrnkidn = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Cancer' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_cncr = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Chronic Obstructive Pulmonary Disease' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_copd = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Depression' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_depressn = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Diabetes' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_diabetes = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Ischemic Heart Disease' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_ischmcht = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Osteoporosis' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_osteoprs = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Arthritis' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_ra_oa = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5
                 UNION ALL
                 SELECT   'Stroke' AS condition,
                          county_name,
                          state_name,
                          race,
                          sex_label,
                          cast(avg(age) AS int) AS avg_age,
                          count(*)              AS cnt
                 FROM     `cs-6440.bfs.sample_data_labels`
                 WHERE    sp_strketia = 1
                 GROUP BY 1,
                          2,
                          3,
                          4,
                          5 

—this IS the dataset weUSE for data5.xlsx WITH condition_counts AS
                          (
                                   SELECT   desynpuf_id,
                                            state_name,
                                            count(DISTINCT condition) AS num_conditions
                                   FROM     `cs-6440.bfs.sample_data_agg_per`
                                   GROUP BY desynpuf_id,
                                            state_name ),
                          bucketed AS
                          (
                                   SELECT   state_name,
                                            CASE
                                                     WHEN num_conditions = 0 THEN '0 conditions'
                                                     WHEN num_conditions = 1 THEN '1 condition'
                                                     WHEN num_conditions = 2 THEN '2 conditions'
                                                     ELSE '3+ conditions'
                                            END      AS complexity_group,
                                            count(*) AS patient_count
                                   FROM     condition_counts
                                   GROUP BY state_name,
                                            complexity_group ),
                          totals AS
                          (
                                   SELECT   state_name,
                                            sum(patient_count) AS total_patients
                                   FROM     bucketed
                                   GROUP BY state_name )SELECT   b.state_name,
                          b.complexity_group,
                          b.patient_count,
                          Safe_divide(b.patient_count, t.total_patients) AS pct_of_population
                 FROM     bucketed b
                 JOIN     totals t
                 ON       b.state_name = t.state_name
                 ORDER BY state_name,
                          complexity_group;

—this IS the dataset we used FOR data4.xlsx WITH base AS
                 (
                                 SELECT DISTINCT desynpuf_id,
                                                 condition,
                                                 state_name
                                 FROM            `cs-6440.bfs.sample_data_agg_per`
                                 WHERE           condition IS NOT NULL ), pairs AS
                 (
                          SELECT   a.state_name,
                                   a.condition                   AS condition_a,
                                   b.condition                   AS condition_b,
                                   count(DISTINCT a.desynpuf_id) AS both_con
                          FROM     base a
                          JOIN     base b
                          ON       a.desynpuf_id = b.desynpuf_id
                          AND      a.state_name = b.state_name
                          GROUP BY 1,
                                   2,
                                   3 ), totals AS
                 (
                          SELECT   state_name,
                                   condition                   AS condition_name,
                                   count(DISTINCT desynpuf_id) AS t.total_patients
                          FROM     base
                          GROUP BY 1,
                                   2 )SELECT   p.state_name,
                          p.condition_a,
                          p.condition_b,
                          both_con,
                          t.total_patients                        AS total_patients_with_condition,
                          Safe_divide(both_con, t.total_patients) AS comorbidity_rate
                 FROM     pairs p
                 JOIN     totals t
                 ON       p.state_name = t.state_name
                 AND      p.condition_a = t.condition_name
                 ORDER BY state_name,
                          condition_a,
                          condition_b;

—-this IS the query we used TO build data3.csv
— this table is the same as data2 but by each user
                 CREATE OR replace TABLE `cs-6440.bfs.sample_data_agg_per` ASSELECT 'Alzheimer'  AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_alzhdmta = 1
                 UNION ALL
                 SELECT 'Heart Failure' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_chf = 1
                 UNION ALL
                 SELECT 'Chronic Kidney Disease' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_chrnkidn = 1
                 UNION ALL
                 SELECT 'Cancer' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_cncr = 1
                 UNION ALL
                 SELECT 'Chronic Obstructive Pulmonary Disease' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_copd = 1
                 UNION ALL
                 SELECT 'Depression' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_depressn = 1
                 UNION ALL
                 SELECT 'Diabetes' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_diabetes = 1
                 UNION ALL
                 SELECT 'Ischemic Heart Disease' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_ischmcht = 1
                 UNION ALL
                 SELECT 'Osteoporosis' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_osteoprs = 1
                 UNION ALL
                 SELECT 'Arthritis' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_ra_oa = 1
                 UNION ALL
                 SELECT 'Stroke' AS condition,
                        county_name,
                        state_name,
                        race,
                        sex_label,
                        desynpuf_id,
                        age
                 FROM   `cs-6440.bfs.sample_data_labels`
                 WHERE  sp_strketia = 1
